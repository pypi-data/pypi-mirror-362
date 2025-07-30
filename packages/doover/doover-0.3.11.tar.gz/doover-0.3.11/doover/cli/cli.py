import argparse
import inspect
import json
import os
import pathlib
import platform
import re
import shutil
import stat
import tarfile
import time
import traceback
import uuid
import importlib

import logging
import os
import sys
# import absl.logging

from concurrent.futures import ThreadPoolExecutor, as_completed

from datetime import datetime, timedelta, timezone
from getpass import getpass
from typing import Optional

import requests

try:
    from fuzzywuzzy import process
    # from simple_term_menu import TerminalMenu
except ImportError:
    process = None
    print("Fuzzywuzzy and/or simple_term_menu not installed. CLI functionality may be limited.")
TerminalMenu = None

from . import parsers
from ..cloud.api import Client, Forbidden, NotFound
from ..cloud.api.channel import Processor, Task
from ..cloud.api.message import Message

from .config import ConfigEntry, ConfigManager, NotSet
from .decorators import command, annotate_arg

from .sub_section import SubSection


DEFAULT_HTTP_DOMAIN = "n1.doover.ngrok.app"
DEFAULT_TCP_DOMAIN = "1.tcp.au.ngrok.io:27735"
TUNNEL_URI_MATCH = re.compile(r"(?P<protocol>(tcp|https))://(?P<host>.*):(?P<port>.*)")
KEY_MATCH = re.compile(r"[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}")


class CLI:
    def __init__(self, profile: str = "default", agent: str = None):
        parser = argparse.ArgumentParser(prog="doover", description="Tools for helping with doover.")
        # parser.add_argument("--version", action="version", version=f"doover")
        parser.set_defaults(callback=parser.print_help)

        self.subparser = parser.add_subparsers(dest="subcommand", title="Subcommands")
        self.setup_commands(self.subparser)
        
        self.added_subsections = []

        # to stop circular imports...
        try:
            # fixme: make a [docker] extra feature / package which processors can choose not to install.
            from ..docker.platform import PlatformInterface
            from ..docker.device_agent import DeviceAgentInterface
            from ..docker.tunnel import TunnelInterface
            from ..docker.camera import CameraInterface
            from ..docker.modbus import ModbusInterface
        except ImportError:
            print("Docker interfaces not found. GRPC CLI support will not be available.")
        else:
            self.add_grpc_subsection(SubSection(PlatformInterface, name="platform", description="Interact with a running Platform Interface container"))
            self.add_grpc_subsection(SubSection(DeviceAgentInterface, name="device_agent", description="Interact with a running Device Agent container"))
            self.add_grpc_subsection(SubSection(TunnelInterface, name="tunnel", description="Interact with a running Tunnel Interface container"))
            self.add_grpc_subsection(SubSection(CameraInterface, name="camera", description="Interact with a running Camera Interface container"))
            self.add_grpc_subsection(SubSection(ModbusInterface, name="modbus", description="Interact with a running Modbus Interface container"))
        
        self.args = args = parser.parse_args()

        self.config_manager = ConfigManager()
        self.config_manager.current_profile = getattr(args, "profile", profile)
        self.api: Optional[Client] = None

        if hasattr(args, "agent_id"):
            self.agent_id = args.agent_id if args.agent_id != "default" else agent
        else:
            self.agent_id = None

        if hasattr(args, "agent"):
            self.agent_query = args.agent if args.agent != "default" else None
        else:
            self.agent_query = None
            
        # remove grcp logging while using cli
        os.environ["GRPC_VERBOSITY"] = "ERROR"
        os.environ["GRPC_TRACE"] = ""
        logging.getLogger().setLevel(logging.ERROR)
        sys.stdout.reconfigure(line_buffering=True)

        try:
            passed_args = {
                k: v for k, v in vars(args).items() if k in inspect.signature(args.callback).parameters.keys()
            }
            if ("kwargs" in inspect.signature(args.callback).parameters.keys()):
                passed_args = {
                    k: v for k, v in vars(args).items()
                }
            args.callback(**passed_args)
        except Exception as e:
            self.on_error(e)

    def add_grpc_subsection(self, subsection: SubSection):
        subsection.mount_sub_section(self.subparser)
        self.added_subsections.append(subsection)

    def setup_commands(self, subparser):

        
        for name, func in inspect.getmembers(self, predicate=inspect.ismethod):
            if not getattr(func, "_is_command", False):
                continue

            parser = subparser.add_parser(func._command_name, help=func._command_help)
            parser.set_defaults(callback=func)
            argspec = inspect.signature(func)
            arg_docs = func._command_arg_docs

            for param in argspec.parameters.values():
                kwargs = {"help": arg_docs.get(param.name)}
                param_name = param.name

                if param.default is not inspect.Parameter.empty:
                    kwargs["default"] = param.default
                    kwargs["required"] = False
                    param_name = "--" + param_name

                if param.annotation is parsers.BoolFlag:
                    kwargs["action"] = "store_false" if kwargs["default"] is True else "store_true"
                elif param.annotation is not inspect.Parameter.empty:
                    kwargs["type"] = param.annotation

                parser.add_argument(param_name, **kwargs)

            if func._command_setup_api:
                parser.add_argument("--profile", help="Config profile to use.", default="default")
                parser.add_argument("--agent", help="Agent query string (name or ID) to use for this request.", type=str, default="default")

            parser.add_argument("--enable-traceback", help=argparse.SUPPRESS, default=False, action="store_true")

    def setup_api(self, read: bool = True):
        if read:
            self.config_manager.read()

        config = self.config_manager.current
        if not config:
            raise RuntimeError(f"No configuration found for profile {self.config_manager.current_profile}. "
                               f"Please use a different profile or run `doover login`")

        if self.agent_id is None:
            self.agent_id = config.agent_id

        self.api: Client = Client(
            config.username,
            config.password,
            config.token,
            config.token_expires,
            config.base_url,
            self.agent_id,
            login_callback=self.on_api_login,
        )
        if not (config.token and config.token_expires > datetime.utcnow()):
            self.api.login()

        if self.agent_query is not None:
            self.agent = self.resolve_agent_query(self.agent_query)
            if self.agent is not None:
                self.agent_id = self.api.agent_id = self.agent and self.agent.id
        else:
            self.agent = None

    def resolve_agent_query(self, query_string: str):
        id_match = KEY_MATCH.search(query_string)
        if id_match:
            return self.api.get_agent(id_match.group(0))

        if not (process or TerminalMenu):
            print("Tried to use fuzzy matching without packages installed. "
                  "Please pass an agent ID, or install the extra packages.")
            return

        print("Fetching agents...")
        agents = {a.name: a for a in self.api.get_agent_list()}
        matches = process.extractBests(query_string, agents.keys(), limit=5, score_cutoff=65)
        if len(matches) == 0:
            print(f"Could not resolve agent query: {query_string}. Using default user agent ID.")
            return

        if len(matches) == 1 or len([m for m in matches if m[1] == 100]):
            agent_name, score = matches[0]
            # quick route, no menu required
            print(f"Using agent {agent_name} for API calls. (Query: {query_string}, Score: {score}%)")
            return agents[agent_name]

        options = [f"{m[0]} (Match: {m[1]}%)" for m in matches]
        menu = TerminalMenu(options, title="Select an agent:")
        selected = options[menu.show()]
        agent_name = re.search(r"(.*) \(Match: \d+%\)", selected).group(1)
        print(f"Using agent {agent_name} for API calls. (Query: {query_string})")
        return agents[agent_name]

    def on_api_login(self):
        config: ConfigEntry = self.config_manager.current

        config.agent_id = self.api.agent_id
        config.token = self.api.access_token.token
        config.token_expires = self.api.access_token.expires_at

        self.config_manager.write()

        if self.agent_id is None:
            self.agent_id = config.agent_id

    def on_error(self, exception):
        if isinstance(exception, NotFound):
            print("We couldn't find what you're looking for! Perhaps try a different Agent ID, or check your spelling?")

        elif isinstance(exception, Forbidden):
            print("Uh-oh - you don't have access to that. Perhaps try a different Agent ID, or ask for permissions?")

        elif isinstance(exception, PermissionError):
            print("Looks like you tried to do something to a file you don't have access to. Perhaps try with sudo?")

        else:
            print(f"Hmm... something went wrong: {exception}\n\nPerhaps you can understand more than me?")

        if not self.args.enable_traceback:
            print("Try running with --enable-traceback flag to see the full error.")
        else:
            traceback.print_exc()

    @command(description="Login to your doover account with a username / password")
    def login(self):
        username = input("Please enter your username: ").strip()
        password = getpass("Please enter your password: ").strip()
        base_url = input("Please enter the base API URL: ").strip("%").strip("/")
        profile_name = input("Please enter this profile name (defaults to default): ").strip()
        profile = profile_name if profile_name != "" else "default"

        self.config_manager.create(ConfigEntry(
            profile,
            username=username,
            password=password,
            base_url=base_url,
        ))
        self.config_manager.current_profile = profile

        try:
            self.setup_api(read=False)
            # self.api.login()
        except Exception:
            print("Login failed. Please try again.")
            if self.args.enable_traceback:
                traceback.print_exc()
            return self.login()

        self.config_manager.write()
        print("Login successful.")

    @command()
    def configure_token(self):
        """Configure your doover credentials with a long-lived token"""
        self.configure_token_impl()

    def configure_token_impl(
            self, token: str = None, agent_id: str = None, base_url: str = None, expiry=NotSet, overwrite: bool = False
    ):
        if not token:
            token = input("Please enter your agent token: ").strip()
            # self.config_manager.current.token = token.strip()
        if not agent_id:
            agent_id = input("Please enter your Agent ID: ").strip()
            # self.config_manager.agent_id = agent_id.strip()
        if not base_url:
            base_url = input("Please enter your base API url: ").strip("%").strip("/")
            # self.config.base_url = base_url
        if expiry is NotSet:
            print("This token is intended to be a long-lived token."
                  "I will remind you to reconfigure the token when this expiry is exceeded.")
            expiry_days = input("Please enter the number of days (approximately) until expiration: ")
            try:
                expiry = datetime.utcnow() + timedelta(days=int(expiry_days))
            except ValueError:
                print("I couldn't parse that expiry. I will set it to None which means no expiry.")
                expiry = None

            # self.config.token_expiry = expiry

        profile_name = input("Please enter this profile's name [default]: ")
        profile = profile_name or "default"

        if profile in self.config_manager.entries and not overwrite:
            p = input("There's already a config entry with this profile. Do you want to overwrite it? [y/N]")
            if not p.startswith("y"):
                print("Exitting...")
                return

        self.config_manager.create(ConfigEntry(
            profile, token=token, token_expires=expiry, base_url=base_url, agent_id=agent_id
        ))
        self.config_manager.current_profile = profile

        self.setup_api(read=False)
        try:
            self.api.get_agent(self.agent_id)
        except Forbidden:
            print("Agent token was incorrect. Please try again.")
            return self.configure_token_impl(agent_id=agent_id, base_url=base_url, expiry=expiry, overwrite=True)
        except NotFound:
            print("Agent ID or Base URL was incorrect. Please try again.")
            return self.configure_token_impl(token=token, expiry=expiry, overwrite=True)
        except Exception:
            print("Base URL was incorrect. Please try again.")
            return self.configure_token_impl(token=token, agent_id=agent_id, expiry=expiry, overwrite=True)
        else:
            self.config_manager.write()
            print("Successfully configured doover credentials.")

    @staticmethod
    def format_agent_info(agent):
        fmt = f"""
        Agent Name: {agent.name}
        Agent Type: {agent.type}
        Agent Owner: {agent.owner_org}
        Agent ID: {agent.id}
        """
        return fmt

    @staticmethod
    def format_channel_info(channel):
        fmt = f"""
        Channel Name: {channel.name}
        Channel Type: {str(channel.__class__.__name__)}
        Channel ID: {channel.id}

        Agent ID: {channel.agent_id}
        """
        # Agent Name: {channel.fetch_agent()}

        if isinstance(channel, Task) and channel.processor_id is not None:
            proc = channel.fetch_processor()
            fmt += f"""
        Processor ID: {channel.processor_id}
        Processor Name: {proc.name}
        """
        fmt += f"""
        Aggregate: {json.dumps(channel.aggregate, indent=4)}
        """
        return fmt

    @command(description="List available agents", setup_api=True)
    def get_agent_list(self):
        agents = self.api.get_agent_list()
        for a in agents:
            print(self.format_agent_info(a))

    @command(description="Get channel info", setup_api=True)
    @annotate_arg("channel_name", "Channel name to get info for")
    def get_channel(self, channel_name: str):
        try:
            channel = self.api.get_channel(channel_name)
        except NotFound:
            print(channel_name, self.agent_id)
            channel = self.api.get_channel_named(channel_name, self.agent_id)

        print(self.format_channel_info(channel))

    @command(setup_api=True)
    @annotate_arg("channel_name", "Channel name to create")
    def create_channel(self, channel_name: str):
        """Create new channel"""
        channel = self.api.create_channel(channel_name, self.agent_id)
        print(f"Channel created successfully. ID: {channel.id}")
        print(self.format_channel_info(channel))

    @command(setup_api=True)
    @annotate_arg("task_name", "Task channel name to create.")
    @annotate_arg("processor_name", "Processor name for this task to trigger.")
    def create_task(self, task_name: parsers.task_name, processor_name: parsers.processor_name):
        """Create new task channel."""
        processor = self.api.get_channel_named(processor_name, self.agent_id)
        task = self.api.create_task(task_name, self.agent_id, processor.id)
        print(f"Task created successfully. ID: {task.id}")
        print(self.format_channel_info(task))

    @command(setup_api=True)
    @annotate_arg("task_name", "Task channel name to create.")
    @annotate_arg("package_path", "Path to the  processor package to publish")
    @annotate_arg("channel_name", "[Optional] take the last message from this channel to start the task.")
    @annotate_arg("csv_file", "[Optional] Path to a CSV export of messages to run the task on.")
    @annotate_arg("parallel_processes", "[Optional] Number of parallel processes to run the task with.")
    @annotate_arg("dry_run", "Whether to run the task without invoking it.")
    def invoke_local_task(self,
                            task_name: parsers.task_name,
                            package_path: pathlib.Path,
                            channel_name: Optional[str] = None,
                            csv_file: pathlib.Path = None,
                            parallel_processes: int = None,
                            dry_run: bool = False):
        """Invoke a task locally."""
        task_name = "!" + task_name.lstrip('!')
        task = self.api.get_channel_named(task_name, self.agent_id)
        if not isinstance(task, Task):
            print("That wasn't a task channel. Try again?")
            return
        print(self.format_channel_info(task))

        agent = self.api.get_agent(self.agent_id)

        def run_for_single_message(msg_obj, *args, **kwargs):
            if dry_run:
                return "Dry run successful. Task not invoked."
            msg_dict = msg_obj.to_dict() if msg_obj else None
            task.invoke_locally(
                package_path,
                msg_dict,
                {"deployment_config": agent.deployment_config}
            )
            output = f"Task invoked successfully. Message ID: {msg_obj.id if msg_obj else None}."
            if kwargs:
                output = output + f" Extra kwargs: {kwargs}"
            return output

        if csv_file is not None:
            messages = Message.from_csv_export(self.api, csv_file)
            print(f"Loaded {len(messages)} messages from CSV export.")

            if not parallel_processes or parallel_processes == 1:
                for msg in messages:
                    print(f"\nRunning task for message: {msg.id}, with timestamp: {msg.timestamp}. {messages.index(msg) + 1}/{len(messages)}\n")
                    run_for_single_message(msg)
            else:
                with ThreadPoolExecutor(max_workers=parallel_processes) as executor:
                    futures = [executor.submit(run_for_single_message, msg, task_num=messages.index(msg), total_tasks=len(messages)) for msg in messages]
                    for future in as_completed(futures):
                        print(future.result())

        else:

            msg_obj = None
            if channel_name:
                channel = self.api.get_channel_named(channel_name, self.agent_id)
                msg_obj = channel.last_message

            if not msg_obj:
                print("No message found. running task without a message.")
            else:
                print(f"\nRunning task for message: {msg_obj.id}, with timestamp: {msg_obj.timestamp}\n")
            run_for_single_message(msg_obj)

    @command(setup_api=True)
    @annotate_arg("module_path", "Path to the python report generator module to compose")
    @annotate_arg("period_from", "Start of the period to report on")
    @annotate_arg("period_to", "End of the period to report on")
    @annotate_arg("agent_ids", "Agent IDs to run the report on")
    @annotate_arg("agent_names", "Agent display names to run the report on")
    def compose_report(self,
                        period_from: datetime = datetime.now() - timedelta(days=7),
                        period_to: datetime = None,
                        agent_ids: str = "",
                        agent_names: str = "",
                        package_path: str = "pydoover.reports.xlsx_base",
                    ):
        """
        Compose a report locally.
        
        Example Usage:
        pydoover compose_report --agent_ids "abcdefg,abdfgds" --agent_names "Agent 1,Agent 2"
        """

        if isinstance(agent_ids, str):
            agent_ids = agent_ids.split(",")
        if isinstance(agent_names, str):
            agent_names = agent_names.split(",")

        ## Attempt necessary imports
        import pytz
        import tzlocal

        module = importlib.import_module(package_path)

        # Retrieve the report generator class from the imported module.
        # Here we assume the class is named "Generator". Adjust if necessary.
        ReportGeneratorClass = getattr(module, "generator", None)
        if ReportGeneratorClass is None:
            print("No 'Generator' found in the specified module!")
            return

        # If period_to is not provided, default to now.
        if period_to is None:
            period_to = datetime.now(timezone.utc)

        # Define additional parameters for instantiation.
        tmp_workspace = "/tmp/doover_report_output/"  # Adjust as needed
        access_token = self.config_manager.current.token  # Provide valid access token
        api_endpoint = self.config_manager.current.base_url  # Provide valid endpoint
        report_name = "Local Report"
        test_mode = False  # Set as needed

        # Clear and recreate the temporary workspace.
        if os.path.exists(tmp_workspace):
            shutil.rmtree(tmp_workspace)
        os.makedirs(tmp_workspace)

        # Get the local timezone as a pytz object
        local_tz_name = tzlocal.get_localzone_name()
        for_timezone = pytz.timezone(local_tz_name)

        def progress_update(progress: int):
            if progress is not None:
                print(f"Progress: {progress* 100}%")

        # Instantiate the report generator.
        report_instance = ReportGeneratorClass(
            tmp_workspace=tmp_workspace,
            access_token=access_token,
            agent_ids=agent_ids,
            agent_display_names=agent_names,
            period_from_utc=period_from.astimezone(timezone.utc),
            period_to_utc=period_to.astimezone(timezone.utc),
            for_timezone=for_timezone,
            logging_function=print,
            progress_update_function=progress_update,
            api_endpoint=api_endpoint,
            report_name=report_name,
            test_mode=test_mode
        )

        # Invoke the report generation.
        report_instance.generate()
        print("Report composed successfully!")
        print(f"Output saved to: {tmp_workspace}")

    @command(setup_api=True)
    def create_processor(self, processor_name: parsers.processor_name):
        """Create new processor channel."""
        processor = self.api.create_processor(processor_name, self.agent_id)
        print(f"Processor created successfully. ID: {processor.id}")
        print(self.format_channel_info(processor))

    @command(setup_api=True)
    @annotate_arg("channel_name", "Channel name to publish to")
    def publish(self, channel_name: str, message: parsers.maybe_json):
        """Publish to a doover channel."""
        try:
            channel = self.api.get_channel_named(channel_name, self.agent_id)
        except NotFound:
            print("Channel name was incorrect. Is it owned by this agent?")
            return

        if isinstance(message, dict):
            print("Successfully loaded message as JSON.")

        channel.publish(message)
        print("Successfully published message.")

    @command(setup_api=True)
    @annotate_arg("channel_name", "Channel name to publish to")
    @annotate_arg("file_path", "Path to the file to publish")
    def publish_file(self, channel_name: str, file_path: pathlib.Path):
        """Publish file to a processor channel."""
        if not file_path.exists():
            print("File path was incorrect.")
            return

        try:
            channel = self.api.get_channel_named(channel_name, self.agent_id)
        except NotFound:
            print("Channel name was incorrect. Is it owned by this agent?")
            return

        channel.update_from_file(file_path)
        print("Successfully published new file.")

    @command(setup_api=True)
    @annotate_arg("processor_name", "Processor channel name to publish to")
    @annotate_arg("package_path", "Path to the package to publish")
    def publish_processor(self, processor_name: parsers.processor_name, package_path: pathlib.Path):
        """Publish processor package to a processor channel."""
        if not package_path.exists():
            print("Package path was incorrect.")
            return

        try:
            channel = self.api.get_channel_named(processor_name, self.agent_id)
        except NotFound:
            print("Channel name was incorrect. Is it owned by this agent?")
            return

        if not isinstance(channel, Processor):
            print("Channel name is not a processor. Try a different name?")
            return

        channel.update_from_package(package_path)
        print("Successfully published new package.")

    @command(setup_api=True)
    @annotate_arg("channel_name", "Channel name to publish to")
    @annotate_arg("poll_rate", "Frequency to check for new messages (in seconds)")
    def follow_channel(self, channel_name: str, poll_rate: int = 5):
        """Follow aggregate of a doover channel"""
        channel = self.api.get_channel_named(channel_name, self.agent_id)
        print(self.format_channel_info(channel))

        while True:
            old_aggregate = channel.aggregate
            channel.update()
            if channel.aggregate != old_aggregate:
                print(channel.aggregate)

            time.sleep(poll_rate)

    @command(setup_api=True)
    @annotate_arg("task_name", "Task name to add the subscription to")
    @annotate_arg("channel_name", "Channel name to subscribe to")
    def subscribe_channel(self, task_name: parsers.task_name, channel_name: str):
        """Add a channel to a task's subscriptions."""
        task = self.api.get_channel_named(task_name, self.agent_id)
        if not isinstance(task, Task):
            print("That wasn't a task channel. Try again?")
            return

        channel = self.api.get_channel_named(channel_name, self.agent_id)
        task.subscribe_to_channel(channel.id)
        print(f"Successfully added {channel_name} to {task.name}'s subscriptions.")

    @command(setup_api=True)
    @annotate_arg("task_name", "Task name to remove the subscription from")
    @annotate_arg("channel_name", "Channel name to unsubscribe from")
    def unsubscribe_channel(self, task_name: parsers.task_name, channel_name: str):
        """Remove a channel to a task's subscriptions."""
        task = self.api.get_channel_named(task_name, self.agent_id)
        if not isinstance(task, Task):
            print("That wasn't a task channel. Try again?")
            return

        channel = self.api.get_channel_named(channel_name, self.agent_id)
        task.unsubscribe_from_channel(channel.id)
        print(f"Successfully removed {channel_name} from {task.name}'s subscriptions.")

    @command(setup_api=True)
    @annotate_arg("config_file", "Deployment config file to use. This is usually a doover_config.json file.")
    def deploy_config(self, config_file: pathlib.Path):
        """Deploy a doover config file to the site."""
        if not config_file.exists():
            print("Config file not found.")
            return

        parent_dir = os.path.dirname(config_file)

        with open(config_file, "r") as config_file:
            data = json.loads(config_file.read())

        print("Read config file.")

        proc_deploy_data = data.get("processor_deployments")
        if proc_deploy_data:
            for processor_data in proc_deploy_data.get("processors", []):
                processor = self.api.create_processor(processor_data["name"], self.agent_id)
                processor.update_from_package(os.path.join(parent_dir, processor_data["processor_package_dir"]))
                processor.update()
                print(f"Created or updated processor {processor.name} with processor data length: {len(processor.aggregate)}")

            for task_data in proc_deploy_data.get("tasks", []):
                processor = self.api.get_channel_named(task_data["processor_name"], self.agent_id)
                task = self.api.create_task(task_data["name"], self.agent_id, processor.id)
                task.publish(task_data["task_config"])
                print(f"Created or updated task {task.name}, and deployed new config.")

                for subscription in task_data.get("subscriptions", []):
                    channel = self.api.create_channel(subscription["channel_name"], self.agent_id)
                    if subscription["is_active"] is True:
                        task.subscribe_to_channel(channel.id)
                        print(f"Added {channel.name} as a subscription to task {task.name}.")
                    else:
                        task.unsubscribe_from_channel(channel.id)
                        print(f"Removed {channel.name} as a subscription from task {task.name}.")

        file_deploy_data = data.get("file_deployments")
        if file_deploy_data:
            for entry in file_deploy_data.get("files", []):
                channel = self.api.create_channel(entry["name"], self.agent_id)
                mime_type = entry.get("mime_type", None)
                channel.update_from_file(os.path.join(parent_dir, entry["file_dir"]), mime_type)
                print(f"Published file to {channel.name}")

        for entry in data.get("deployment_channel_messages", []):
            channel = self.api.create_channel(entry["channel_name"], self.agent_id)
            save_log = entry.get("save_log", True)
            channel.publish(entry["channel_message"], save_log=save_log)
            print(f"Published message to {channel.name}")

        print("Successfully deployed config.")

    @staticmethod
    def _get_ip():
        return requests.get("https://api.ipify.org").text

    def _create_tunnel(
        self, hostname: str, port: int,
        protocol: str, timeout: int,
        restrict_cidr: bool = True
    ):
        tunnels = self.api.get_tunnels(self.agent_id)
        if restrict_cidr:
            my_ip = self._get_ip()

        tunnel = None
        for t in tunnels["tunnels"]:
            if t["hostname"] == hostname and t["port"] == port:
                tunnel = t
                break

        if tunnel:
            if tunnel["timeout"] != timeout or tunnel["ip_restricted"] != restrict_cidr or (restrict_cidr and my_ip not in tunnel["ip_whitelist"]):
                print("Existing tunnel found, but with different settings. Editting tunnel...")
                self.api.patch_tunnel(
                    tunnel["key"],
                    timeout=timeout,
                    ip_restricted=restrict_cidr,
                    ip_whitelist=[my_ip] if restrict_cidr else [],
                )
            print(f"Found existing tunnel: {tunnel['endpoint']}...")
            return tunnel

        print("No tunnel found. Opening tunnel... Please wait...")
        tunnel = self.api.create_tunnel(
            self.agent_id,
            hostname=hostname,
            port=port,
            protocol=protocol,
            name=f"{hostname}:{port}",
            ip_restricted=restrict_cidr,
            is_favourite=True,
            ip_whitelist=[my_ip] if restrict_cidr else [],
            timeout=timeout,
        )

        return tunnel

    def _activate_tunnel(self, tunnel_id, wait_for_open: bool = True):
        self.api.activate_tunnel(tunnel_id)
        print(f"Activated tunnel {tunnel_id}.")

        if wait_for_open:
            print("Waiting for tunnel to open...")
            while True:
                tunnel = self.api.get_tunnel(tunnel_id)
                if tunnel["is_active"]:
                    print("Tunnel is open.")
                    break

                time.sleep(1)

    @command(description="Open an SSH tunnel for a doover agent", setup_api=True)
    def open_ssh_tunnel(self, timeout: int = 15, restrict_cidr: bool = True):
        tunnel = self._create_tunnel("127.0.0.1", 22, "tcp", timeout, restrict_cidr)
        print(tunnel)
        if not tunnel["is_active"]:
            self._activate_tunnel(tunnel["key"], True)

        host, port = tunnel["endpoint"].split(":")

        username = input("Please enter your SSH username: ")

        print(f"Opening SSH session with host: {host}, port: {port}, username: {username}...")
        os.execl("/usr/bin/ssh", "ssh", f"{username}@{host}", "-p", port)

    @command(description="Open an arbitrary tunnel for a doover agent", setup_api=True)
    def open_tunnel(self, address: str, protocol: str = "http", timeout: int = 15, restrict_cidr: bool = True):
        host, port = address.split(":")
        self._create_tunnel(host, int(port), protocol, timeout, restrict_cidr)

    @command(description="Close all tunnels for a doover agent", setup_api=True)
    def close_all_tunnels(self):
        channel = self.api.get_channel_named("tunnels", self.agent_id)
        channel.publish({"to_close": channel.aggregate["open"]})
        print("Successfully closed all tunnels.")

    def _activate_deactivate_tunnel(self, tunnel_id: str = None, activate: bool = True):
        action = self.api.activate_tunnel if activate else self.api.deactivate_tunnel
        action_word = "activate" if activate else "deactivate"

        if tunnel_id:
            action(tunnel_id)
            print(f"Successfully {'activated' if activate else 'deactivated'} tunnel.")
            return

        tunnels = self.api.get_tunnels(self.agent_id)
        if not tunnels.get("tunnels", []):
            print("No tunnels found.")
            return

        options = [f"{tunnel['name']} ({tunnel['endpoint']})" for tunnel in tunnels["tunnels"]]
        menu = TerminalMenu(options, title="Select an agent:")
        tunnel = tunnels["tunnels"][menu.show()]
        action(tunnel['key'])
        print(f"Successfully {action_word} tunnel.")

    @command(description="Get tunnels for an agent", setup_api=True)
    def get_tunnels(self):
        tunnels = self.api.get_tunnels(self.agent_id)
        for tunnel in tunnels["tunnels"]:
            print(f"{tunnel['name']} ({tunnel['endpoint']}) - {'Active' if tunnel['is_active'] else 'Inactive'}")

    @command(description="Activate a tunnel", setup_api=True)
    def activate_tunnel(self, tunnel_id: str = None):
        self._activate_deactivate_tunnel(tunnel_id, activate=True)

    @command(description="Deactivate a tunnel", setup_api=True)
    def deactivate_tunnel(self, tunnel_id: str = None):
        self._activate_deactivate_tunnel(tunnel_id, activate=False)

    # @command(description="Create new tunnel endpoints for an agent", setup_api=True)
    # def create_tunnel_endpoints(self, endpoint_type: str = "tcp", amount: int = 1):
    #     if endpoint_type not in ("tcp", "http"):
    #         print("Endpoint type must be either tcp or http.")
    #         return
    #
    #     if amount < 1:
    #         print("Amount must be a number greater than or equal to 1.")
    #         return
    #
    #     data = self.api.create_tunnel_endpoints(self.agent_id, endpoint_type, amount)
    #     for d in data:
    #         print(f"Created new {endpoint_type} endpoint: {d}")
    #
    #     channel = self.api.get_channel_named("tunnels", self.agent_id)
    #     key = f"{endpoint_type}_endpoints"
    #     channel.publish({key: channel.aggregate.get(key, []) + data})

    @command(description="List ngrok tunnel endpoints for an agent", setup_api=True)
    def list_tunnel_endpoints(self):
        print("#################\nDEPRECATED##################\n\nYou're probably after the `get_tunnels` command.")
        tcp = self.api.get_tunnel_endpoints(self.agent_id, "tcp")
        http = self.api.get_tunnel_endpoints(self.agent_id, "http")

        print(f"HTTP Endpoints\n==============\n" + '\n'.join(http))
        print(f"TCP Endpoints\n=============\n" + '\n'.join(tcp))


    def main(self):
        pass
