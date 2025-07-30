import asyncio
import json
import logging
import time
import json

from collections.abc import Iterable
from typing import Optional, Callable, Any

import grpc

from .grpc_stubs import platform_iface_pb2, platform_iface_pb2_grpc
from ..grpc_interface import GRPCInterface
from ...utils import maybe_async, call_maybe_async, deprecated
from ...cli.decorators import command as cli_command, annotate_arg

class PulseCounter:
    def __init__(
        self,
        plt_iface: "PlatformInterface",
        pin: int,
        edge: str = "rising",
        callback: Callable[[int, bool, int, int, str], Any] = None,
        rate_window_secs: int = 60,
        auto_start: bool = True,
    ):
        self.platform_iface = plt_iface
        self.pin = pin
        self.edge = edge
        self.callback = callback
        self.rate_window_secs = rate_window_secs
        self.count = 0

        self.start_time = time.time()
        self.pulse_grace_period = 0.2  # Need to ignore pulses for a short period after starting
        self.pulse_timestamps = []
        
        self.recieving_pulses = False
        self.recieving_events = False

        if auto_start:
            self.start_listener_pulses()

    @deprecated("Replaced with PulseCounter.start_listener_pulses")
    def start_listener(self):
        self.start_listener_pulses()
        
    def start_listener_pulses(self):
        
        # Check each pulse counter is only used for a single type of pulse
        if self.recieving_events:
            logging.error("Using a pulse counter for both pulses and offline events")
            return
        self.recieving_pulses = True
        
        self.start_time = time.time()
        self.platform_iface.start_di_pulse_listener(self.pin, self.receive_pulse, edge=self.edge, start_count=self.count)

    def update_events(self):
        
        # Check each pulse counter is only used for a single type of pulse
        if self.recieving_pulses:
            logging.error("Using a pulse counter for both pulses and offline events")
            return
        self.recieving_events = True
        
        self.recieve_events(self.platform_iface.get_di_events(self.pin, self.edge, include_system_events=True))
        
    def add_existing_events(self, time_stamps):
        
        # Check each pulse counter is only used for a single type of pulse
        if self.recieving_pulses:
            logging.error("Using a pulse counter for both pulses and offline events")
            return
        self.recieving_events = True
        
        self.pulse_timestamps += time_stamps
        self.count = len(self.pulse_timestamps)

    async def receive_pulse(self, di, di_value, dt_secs, counter, edge):
        
        # Check each pulse counter is only used for a single type of pulse
        if self.recieving_events:
            logging.error("Using a pulse counter for both pulses and offline events")
            return
        self.recieving_pulses = True
        
        if time.time() - self.start_time < self.pulse_grace_period:
            logging.info("Ignoring pulse on di=" + str(di) + " with dt=" + str(dt_secs) + "s")
            return
        logging.info("Received pulse on di=" + str(di) + " with dt=" + str(dt_secs) + "s")
        self.count += 1
        self.pulse_timestamps += [time.time()]
        if self.callback is not None:
            await call_maybe_async(self.callback, self.pin, di_value, dt_secs, self.count, edge)
            
    def recieve_events(self, events):
        
        # Check each pulse counter is only used for a single type of pulse
        if self.recieving_pulses:
            logging.error("Using a pulse counter for both pulses and offline events")
            return
        self.recieving_events = True
                
        for event in events:
            edge = ""
            di_value = 0
            if event.event == "DI_R":
                di_value = 1
                edge = "rising"
            elif event.event == "DI_F":
                edge = "falling"
            elif event.event == "VI":
                event = "VI"
            else: # Could be a system event
                self.handle_system_event(event)
                continue
            
            timestamp = event.time / 1000 or time.time()
            dt_secs = 0
            if len(self.pulse_timestamps) > 0:
                if timestamp <= self.pulse_timestamps[-1] + 0.01:
                    logging.warning(f"Ignoring old event on di={event.pin} t={timestamp} latest event: {self.pulse_timestamps[-1]}")
                    continue
                dt_secs = timestamp - self.pulse_timestamps[-1]
            logging.info(f"Received event on di={event.pin} with t=" + str(dt_secs) + "s")
            self.count += 1
            self.pulse_timestamps += [timestamp]
            if self.callback is not None:
                self.callback(self.pin, di_value, dt_secs, timestamp, self.count, edge)
    
    def handle_system_event(self, event):
        pass

    @deprecated("Use get_pulses_in_window to not damage record of pulses/events")
    def clean_pulse_timestamps(self):
        if len(self.pulse_timestamps) == 0:
            return

        ## Remove timestamps older than the rate window
        while len(self.pulse_timestamps) > 0 and self.pulse_timestamps[0] < time.time() - self.rate_window_secs:
            self.pulse_timestamps.pop(0)
            
    def get_pulses_in_window(self):
        if len(self.pulse_timestamps) == 0:
            return []

        pulses = []
        ## Remove timestamps older than the rate window
        for timestamp in self.pulse_timestamps:
            if timestamp > self.pulse_timestamps[-1] - self.rate_window_secs:
                pulses.append(timestamp)
        return pulses

    def set_rate_window(self, rate_window_secs):
        self.rate_window_secs = rate_window_secs

    def get_rate_window(self):
        return self.rate_window_secs

    def get_pulses_per_minute(self):
        pulses = self.get_pulses_in_window()
        return len(pulses) * 60 / self.rate_window_secs

    def set_counter(self, counter):
        self.count = counter

    def get_counter(self):
        return self.count
    


class PlatformInterface(GRPCInterface):
    stub = platform_iface_pb2_grpc.platformIfaceStub

    @annotate_arg("plt_uri", "the address that platform interface is running")
    def __init__(self, plt_uri: str = "localhost:50053", is_async: bool = False):
        super().__init__(plt_uri, is_async)
        self.pulse_counter_listeners = []

    def close(self):
        logging.info("Closing platform interface...")
        for listener in self.pulse_counter_listeners:
            listener.cancel()

    def process_response(self, stub_call: str, response, **kwargs):
        response = super().process_response(stub_call, response, **kwargs)

        try:
            response_field = kwargs.pop("response_field")
        except KeyError:
            return response

        res = getattr(response, response_field, None)
        if isinstance(res, Iterable) and not isinstance(res, str):  # don't iterate over strings
            res = list(res)

        if isinstance(res, list) and len(res) == 1:
            return res[0]

        return res

    
    def get_new_pulse_counter(
        self,
        di: int,
        edge: str = "rising",
        callback: Callable[[int, bool, int, int, str], Any] = None,
        rate_window_secs: int = 20,
        auto_start: bool = True
    ) -> PulseCounter:
        return PulseCounter(self, di, edge=edge, callback=callback, rate_window_secs=rate_window_secs, auto_start=auto_start)
    
    def get_new_event_counter(
        self,
        di: int,
        edge: str = "rising",
        callback: Callable[[int, bool, int, int, str], Any] = None,
        rate_window_secs: int = 20,
        auto_collect: bool = True
    ) -> PulseCounter:
        """Create a new Pulse Counter for counting events.
            counter = pltiface.get_new_event_counter(0, "rising")
            print(counter.get_counter())
            print(counter.get_pulses_per_minute())

        Parameters
        ----------
        di : int
            Pin number to check events for.
        edge : "rising" or "falling" or "both"
            The edge to listen to evenets on.
        callback : (pin, di_value, dt_secs, timestamp, count, edge) -> any
            Callback called when an event is processed.
        rate_window_secs : int = 20
            The size of window for which the rate of events is calculated.
        auto_collect : bool = True
            Whether to automatically collect the events from the platform interface.

        Returns
        -------
        PulseCounter object
        """
        counter = PulseCounter(self, di, edge=edge, callback=callback, rate_window_secs=rate_window_secs, auto_start=False)
        if auto_collect:
            counter.update_events()
        return counter

    def start_di_pulse_listener(self, di: int, callback, edge: str = "rising", start_count: int = 0):
        ## Callback should be a function that takes the following arguments:
        ## di, di_value, dt_secs, counter, edge

        listener = asyncio.create_task(self.recv_di_pulses(di, callback, edge=edge, start_count=start_count))
        self.pulse_counter_listeners.append(listener)
        listener.add_done_callback(self.pulse_counter_listeners.remove)
    
    async def recv_di_pulses(self, di: int, callback, edge: str = "rising", start_count: int = 0):
        counter = start_count
        active_callbacks = set()

        while True:
            try:
                # Setup the connection to the platform interface
                async with grpc.aio.insecure_channel(self.uri) as channel:
                    channel_stream = platform_iface_pb2_grpc.platformIfaceStub(channel).startPulseCounter(platform_iface_pb2.pulseCounterRequest(di=di, edge=edge))

                    while True:

                        response = await channel_stream.read()
                        if response is None or response == grpc.aio.EOF:
                            logging.info("pulseCounter for di=" + str(di) + " ended.")
                            break
                        
                        logging.debug("Received response from pulseCounter for di=" + str(di))

                        if hasattr(response, "dt_secs") and response.dt_secs is not None and response.dt_secs > 0:
                            ## Increment the counter
                            counter += 1
                            ## Call the callback function with the response
                            task = await call_maybe_async(callback, di, response.value, response.dt_secs, counter, edge, as_task=True)
                            if task:
                                active_callbacks.add(task)
                                task.add_done_callback(active_callbacks.remove)

            except asyncio.CancelledError:
                logging.info("pulseCounter for di=" + str(di) + " cancelled.")
                break

            except StopAsyncIteration:
                logging.info("pulseCounter for di=" + str(di) + " ended.")
                break

            except Exception as e:
                logging.error("Error receiving pulse for di=" + str(di) + ": " + str(e), exc_info=e)
                # await asyncio.sleep(1)

            ## Loop again
            await asyncio.sleep(1)

        ## Wait for all active callbacks to finish
        while active_callbacks:
            await asyncio.wait(active_callbacks, timeout=1)

    @staticmethod
    def _cast_pins(pins):
        if isinstance(pins, int):
            return [pins]
        elif isinstance(pins, list):
            return pins
        else:
            raise ValueError(f"Invalid type for pins: {type(pins)}. Must be int or list.")
            # logging.error(f"Invalid type for pins: {type(pins)}. Must be int or list."
            # return None

    @staticmethod
    def _cast_values(values):
        if isinstance(values, int):
            return [bool(values)]
        elif isinstance(values, list):
            return [bool(v) for v in values]
        else:
            raise ValueError(f"Invalid type for values: {type(values)}. Must be bool or list.")

    @staticmethod
    def _cast_ao_values(values):
        if isinstance(values, int):
            return [float(values)]
        elif isinstance(values, float):
            return [values]
        elif isinstance(values, list):
            return [float(v) for v in values]
        else:
            raise ValueError(f"Invalid type for values: {type(values)}. Must be float or list.")
        
    def _cast_ao_pin_values(self, pins, values):
        pins = self._cast_pins(pins)
        values = self._cast_ao_values(values)

        if len(pins) != len(values):
            if len(values) == 1:
                values = [values[0]] * len(pins)
            else:
                raise ValueError("Analogue output and value lists are not the same length.")

        return pins, values
    
    def _cast_pin_values(self, pins, values):
        pins = self._cast_pins(pins)
        values = self._cast_values(values)

        if len(pins) != len(values):
            if len(values) == 1:
                values = [values[0]] * len(pins)
            else:
                raise ValueError("Digital output and value lists are not the same length.")

        return pins, values
    
    @cli_command()
    def test_comms(self, message: str = "Comms Check Message") -> Optional[str]:
        """Test connection by sending a basic echo response to platform interface container.

        Parameters
        ----------
        message : str
            Message to send to platform interface to have echo'd as a response

        Returns
        -------
        str
            The response from platform interface.
        """
        return self.make_request("TestComms", platform_iface_pb2.TestCommsRequest(message=message), response_field="response")

    @cli_command()
    @maybe_async()
    def get_di(self, di: int | list[int]) -> Optional[list[bool]]:
        """Get digital input values.

        Parameters
        ----------
        di : int or list
            Pin numbers to get the values of. Can be a single pin number or a list of pin numbers.

        Returns
        -------
        list[bool]
            List of digital input values.
        """
        pins = self._cast_pins(di)
        return self.make_request("getDI", platform_iface_pb2.getDIRequest(di=pins), response_field="di")

    async def get_di_async(self, di: int | list[int]) -> list[bool]:
        pins = self._cast_pins(di)
        return await self.make_request_async("getDI", platform_iface_pb2.getDIRequest(di=pins), response_field="di")

    @cli_command()
    @maybe_async()
    def get_ai(self, ai: int | list[int]) -> Optional[list[float]]:
        """Get analogue input values.

        Parameters
        ----------
        ai : int or list
            Pin numbers to get the values of. Can be a single pin number or a list of pin numbers.

        Returns
        -------
        list[float]
            List of analogue input values.
        """
        # Above section is to facilitate the following:
        # get_ai(1)
        # get_ai([1,4,2])

        # Proposal: get_ai(*pins)
        # allows for get_ai(1, 2, 3) or get_ai(1) or get_ai(*[1, 2, 3])

        pins = self._cast_pins(ai)
        return self.make_request("getAI", platform_iface_pb2.getAIRequest(ai=pins), response_field="ai")

    async def get_ai_async(self, ai: int | list[int]) -> list[float]:
        pins = self._cast_pins(ai)
        return await self.make_request_async("getAI", platform_iface_pb2.getAIRequest(ai=pins), response_field="ai")

    @cli_command()
    @maybe_async()
    def get_do(self, do: int | list[int]) -> Optional[list[bool]]:
        """Get digital output values.

        Parameters
        ----------
        do : int or list
            Pin numbers to get the values of. Can be a single pin number or a list of pin numbers.

        Returns
        -------
        list[bool]
            List of digital output values.
        """
        pins = self._cast_pins(do)
        return self.make_request("getDO", platform_iface_pb2.getDORequest(do=pins), response_field="do")

    async def get_do_async(self, do: int | list[int]) -> list[float]:
        pins = self._cast_pins(do)
        return await self.make_request_async("getDO", platform_iface_pb2.getDORequest(do=pins), response_field="do")

    @cli_command()
    @maybe_async()
    def set_do(self, do: int | list[int], value: int | list[int]) -> Optional[list[bool]]:
        """Set digital output values.

        Parameters
        ----------
        do : int or list
            Pin numbers to set the values of. Can be a single pin number or a list of pin numbers.
        value : int or list
            Values to set the pins to. Can be a single value or a list of values.
            If a single value is provided, all pins will be set to that value.

            .. note::
                The length of the `do` and `value` lists must be the same!

        Returns
        -------
        list[bool]
            ??? Not sure what this is
        """
        pins, values = self._cast_pin_values(do, value)
        return self.make_request("setDO", platform_iface_pb2.setDORequest(do=pins, value=values), response_field="do")

    async def set_do_async(self, do, value):
        pins, values = self._cast_pin_values(do, value)
        return await self.make_request_async("setDO", platform_iface_pb2.setDORequest(do=pins, value=values), response_field="do")

    @cli_command()
    @maybe_async()
    def schedule_do(self, do: int | list[int], value: bool | list[bool], in_secs: int) -> None:
        """Schedule digital output values.

        Parameters
        ----------
        do : int or list
            Pin numbers to set the values of. Can be a single pin number or a list of pin numbers.
        value : int or list
            Values to set the pins to. Can be a single value or a list of values.
            If a single value is provided, all pins will be set to that value.
        in_secs : int
            Time in seconds to schedule the change in digital output values. Must be positive.

        Returns
        -------
        Nothing??
        """
        if not isinstance(in_secs, int) or in_secs < 0:
            raise ValueError(f"Invalid value for in_secs: {in_secs}. Must be a positive integer.")

        pins, values = self._cast_pin_values(do, value)

        # Above section is to facilitate the following:
        # schedule_do(1, 1, 1) => [1],[1],1
        # schedule_do([1,4,2], 0, 1) => [1,4,2], [0,0,0], 1
        # schedule_do([1,4,2], [0,1,0], 1) => [1,4,2], [0,1,0], 1

        return self.make_request("scheduleDO", platform_iface_pb2.scheduleDORequest(do=pins, value=values, time_secs=in_secs), response_field="do")

    async def schedule_do_async(self, do: int | list[int], value: bool | list[bool], in_secs: int) -> None:
        if not isinstance(in_secs, int) or in_secs < 0:
            raise ValueError(f"Invalid value for in_secs: {in_secs}. Must be a positive integer.")

        pins, values = self._cast_pin_values(do, value)
        return await self.make_request_async("scheduleDO", platform_iface_pb2.scheduleDORequest(do=pins, value=values, time_secs=in_secs), response_field="do")

    @cli_command()
    @maybe_async()
    def get_ao(self, ao: int | list[int]) -> Optional[list[float]]:
        """Get analogue output values.

        Parameters
        ----------
        ao : int or list
            Pin numbers to get the values of. Can be a single pin number or a list of pin numbers.

        Returns
        -------
        list[float]
            List of analogue output values.
        """
        pins = self._cast_pins(ao)
        return self.make_request("getAO", platform_iface_pb2.getAORequest(ao=pins), response_field="ao")

    async def get_ao_async(self, ao: int | list[int]) -> list[float]:
        pins = self._cast_pins(ao)
        return await self.make_request_async("getAO", platform_iface_pb2.getAORequest(ao=pins), response_field="ao")

    @cli_command()
    @maybe_async()
    def set_ao(self, ao: int | list[int], value: float | list[float]) -> Optional[list[float]]:
        """Set analogue output values.

        Parameters
        ----------
        ao : int or list[int]
            Pin numbers to set the values of. Can be a single pin number or a list of pin numbers.

        value : bool or list[bool]
            Values to set the pins to. Can be a single value or a list of values.
            If a single value is provided, all pins will be set to that value.

        Returns
        -------
        list[bool]
            List of ouputs set??"""

        # if not isinstance(value, list):
        #     value = [value]
        pins, values = self._cast_ao_pin_values(ao, value)
        return self.make_request("setAO", platform_iface_pb2.setAORequest(ao=pins, value=values), response_field="ao")

    async def set_ao_async(self, ao: int | list[int], value: float | list[float]) -> list[bool]:
        pins, values = self._cast_ao_pin_values(ao, value)
        return await self.make_request_async("setAO", platform_iface_pb2.setAORequest(ao=pins, value=values), response_field="ao")

    @cli_command()
    @maybe_async()
    def schedule_ao(self, ao: int | list[int], value: bool | list[bool], in_secs: int) -> None:
        # fixme: should this function even exist?? setting analog outputs?
        if not isinstance(in_secs, int) or in_secs < 0:
            raise ValueError(f"Invalid value for in_secs: {in_secs}. Must be a positive integer.")

        pins, values = self._cast_ao_pin_values(ao, value)

        # Above section is to facilitate the following:
        # schedule_ao(1, 1, 1) => [1],[1],1
        # schedule_ao([1,4,2], 0, 1) => [1,4,2], [0,0,0], 1
        # schedule_ao([1,4,2], [0,1,0], 1) => [1,4,2], [0,1,0], 1
        return self.make_request(
            "scheduleAO",
            platform_iface_pb2.scheduleAORequest(ao=pins, value=values, time_secs=in_secs),
            response_field="ao"
        )

    async def schedule_ao_async(self, ao: int | list[int], value: bool | list[bool], in_secs: int) -> None:
        if not isinstance(in_secs, int) or in_secs < 0:
            raise ValueError(f"Invalid value for in_secs: {in_secs}. Must be a positive integer.")

        pins, values = self._cast_ao_pin_values(ao, value)
        return await self.make_request_async(
            "scheduleAO",
            platform_iface_pb2.scheduleAORequest(ao=pins, value=values, time_secs=in_secs),
            response_field="ao"
        )

    @cli_command()
    @maybe_async()
    def get_system_voltage(self) -> float:
        return self.make_request("getInputVoltage", platform_iface_pb2.getInputVoltageRequest(), response_field="voltage")

    async def get_system_voltage_async(self) -> float:
        return await self.make_request_async("getInputVoltage", platform_iface_pb2.getInputVoltageRequest(), response_field="voltage")

    @cli_command()
    @maybe_async()
    def get_system_temperature(self):
        return self.make_request("getTemperature", platform_iface_pb2.getTemperatureRequest(), response_field="temperature")

    async def get_system_temperature_async(self):
        return await self.make_request_async("getTemperature", platform_iface_pb2.getTemperatureRequest(), response_field="temperature")

    @cli_command()
    @maybe_async()
    def get_location(self):
        return self.make_request("getLocation", platform_iface_pb2.getLocationRequest(), response_field="location")

    async def get_location_async(self):
        return await self.make_request_async("getLocation", platform_iface_pb2.getLocationRequest(), response_field="location")

    @cli_command()
    @maybe_async()
    def reboot(self):
        return self.make_request("reboot", platform_iface_pb2.rebootRequest())

    async def reboot_async(self):
        # fixme: should these have async varients?
        return await self.make_request_async("reboot", platform_iface_pb2.rebootRequest())

    @cli_command()
    @maybe_async()
    def shutdown(self):
        return self.make_request("shutdown", platform_iface_pb2.shutdownRequest())

    async def shutdown_async(self):
        # fixme: as above
        return await self.make_request_async("shutdown", platform_iface_pb2.shutdownRequest())

    @cli_command()
    @maybe_async()
    def get_immunity_seconds(self):
        return self.make_request("getShutdownImmunity", platform_iface_pb2.getShutdownImmunityRequest(), response_field="immunity_secs")

    async def get_immunity_seconds_async(self):
        return await self.make_request_async("getShutdownImmunity", platform_iface_pb2.getShutdownImmunityRequest(), response_field="immunity_secs")

    @maybe_async()
    def schedule_startup(self, time_secs: int) -> None:
        return self.make_request("scheduleStartup", platform_iface_pb2.scheduleStartupRequest(time_secs=time_secs), response_field="time_secs")

    async def schedule_startup_async(self, time_secs: int) -> None:
        return await self.make_request_async("scheduleStartup", platform_iface_pb2.scheduleStartupRequest(time_secs=time_secs), response_field="time_secs")

    @cli_command()
    @maybe_async()
    def schedule_shutdown(self, time_secs: int) -> None:
        return self.make_request("scheduleShutdown", platform_iface_pb2.scheduleShutdownRequest(time_secs=time_secs), response_field="time_secs")

    async def schedule_shutdown_async(self, time_secs: int) -> None:
        return await self.make_request_async("scheduleShutdown", platform_iface_pb2.scheduleShutdownRequest(time_secs=time_secs), response_field="time_secs")

    @cli_command()
    @maybe_async()
    def get_io_table(self):
        res = self.make_request("getIoTable", platform_iface_pb2.getIoTableRequest(), response_field="io_table")
        # result = json.loads("".join(self.make_request("getIoTable", platform_iface_pb2.getIoTableRequest())))
        if res is None:
            return None
        string = ""
        for i in res:
            string += i
        result = json.loads(string)
        return result
    
    async def get_io_table_async(self):
        res = await self.make_request_async("getIoTable", platform_iface_pb2.getIoTableRequest(), response_field="io_table")
        # result = json.loads("".join(await self.make_request_async("getIoTable", platform_iface_pb2.getIoTableRequest())))
        if res is None:
            return None
        string = ""
        for i in res:
            string += i
        result = json.loads(string)
        return result

    @cli_command()
    @maybe_async()
    def sync_rtc(self):
        return self.make_request("syncRtcTime", platform_iface_pb2.syncRtcTimeRequest())

    async def sync_rtc_async(self):
        return await self.make_request("syncRtcTime", platform_iface_pb2.syncRtcTimeRequest())
    
    @maybe_async()
    def get_events(self, events_from = 0):
        """Get all events.

        Parameters
        ----------
        events_from : None or int
            Starting event id or timestamp (in milliseconds), defaults to all availible.

        Returns
        -------
        list[Event]
            List of events.
        """
        return self.make_request("getEvents", platform_iface_pb2.getEventsRequest(events_from=events_from), response_field="events")

    async def get_events_async(self, events_from = 0):
        return await self.make_request_async("getEvents", platform_iface_pb2.getEventsRequest(events_from=events_from), response_field="events")
    
    @cli_command()
    @maybe_async()
    def get_di_events(self, di_pin, edge, include_system_events = False, events_from = 0):
        """Get di events.

        Parameters
        ----------
        di : int
            Pin number to check events for.
        edge : "rising" or "falling" or "both"
            The edge to listen to evenets on.
        include_system_events : bool = False
            Whether to include system events like for a doovit the cm4 turning on and off or the io board starting up.
        events_from : None or int
            Starting event id or timestamp (in milliseconds), defaults to all availible.

        Returns
        -------
        list[Event]
            List of events for the given digital input pin.
        """
        rising = False
        falling = False
        if edge == "rising":
            rising = True
        elif edge == "falling":
            falling = True
        elif edge == "both":
            rising = True
            falling = True
        return self.make_request("getDIEvents", platform_iface_pb2.getDIEventsRequest(pin=di_pin, rising=rising, falling=falling, include_system_events=include_system_events, events_from=events_from))

    async def get_di_events_async(self, di_pin, edge, include_system_events = False, events_from = 0):
        rising = False
        falling = False
        if edge == "rising":
            rising = True
        elif edge == "falling":
            falling = True
        elif edge == "both":
            rising = True
            falling = True
        return await self.make_request_async("getDIEvents", platform_iface_pb2.getDIEventsRequest(pin=di_pin, rising=rising, falling=falling, include_system_events=include_system_events, events_from=events_from), response_field="events")


platform_iface = PlatformInterface
pulse_counter = PulseCounter
