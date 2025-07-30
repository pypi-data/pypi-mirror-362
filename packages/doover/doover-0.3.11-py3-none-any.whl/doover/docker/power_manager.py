#!/usr/bin/env python3

import asyncio
import logging
import time
from typing import Dict

from ..utils import apply_async_kalman_filter

class PowerManager:
    def __init__(self, app):
        self.app = app
        self.start_time = None
        self.config = {}
        self.scheduled_sleep_time = None ## Secs that the system is scheduled to sleep for
        self.scheduled_goto_sleep_time = None ## Time that the system is scheduled to sleep

        self.last_voltage = None
        self.last_voltage_time = None
        self.voltage_update_interval = 5

        self.soft_watchdog_period_mins = 3 * 60 # 3 hours
        self.last_watchdog_reset_time = None
        self.watchdog_reset_interval_secs = 20

        self.request_shutdown_hooks = [] # Request shutdown hooks will be run and if all return True, the system will shutdown

        self.pre_shutdown_hooks = [] # Pre shutdown hooks will be run when the system schedules a shutdown
        self.shutdown_hooks = [] # Shutdown hooks will be run when the system is about to shutdown

    def register_request_shutdown_hook(self, hook):
        self.request_shutdown_hooks.append(hook)

    def register_pre_shutdown_hook(self, hook):
        self.pre_shutdown_hooks.append(hook)

    def register_shutdown_hook(self, hook):
        self.shutdown_hooks.append(hook)

    async def fetch_config(self):
        self.config = await self.app.get_config_async(key_filter="POWER_MANAGEMENT", wait=True)
        if not self.config or not self.config.get("VOLTAGE_SLEEP_MINUTES"):
            logging.info("No configuration found for PowerManager. Disabling Power Management.")

    def is_active(self):
        return bool(self.config)

    async def update_voltage(self):
        # Only update the voltage every voltage_update_interval seconds
        if self.last_voltage_time is None or asyncio.get_event_loop().time() - self.last_voltage_time > self.voltage_update_interval:
            # self.last_voltage = None
            try:
                self.last_voltage = await self.get_system_voltage()
            except Exception as e:
                logging.error(f"Error fetching system voltage: {e}")

            if self.last_voltage is not None:
                self.last_voltage = round(self.last_voltage, 2)
                self.last_voltage_time = asyncio.get_event_loop().time()
            logging.info(f"Filtered system voltage: {self.last_voltage}")

    @apply_async_kalman_filter(
        process_variance=0.05,
        outlier_threshold=0.5,
    )
    async def get_system_voltage(self) -> float:
        # Get the current system voltage
        voltage = await self.app.platform_iface.get_system_voltage_async()
        return voltage

    def get_sleep_time(self) -> int:
        sorted_config = sorted(self.config.get("VOLTAGE_SLEEP_MINUTES", {}).items())
        voltage = self.last_voltage
        if voltage is None:
            return None
        for threshold, sleep_time in sorted_config:
            if isinstance(threshold, str):
                threshold = float(threshold)
            if voltage <= threshold:
                return sleep_time * 60 # Convert minutes to seconds
        return None
    
    def get_min_awake_time(self) -> int:
        abs_min_awake_time = 60 ## The floor value for the minimum awake time
        min_awake_time = self.config.get("MIN_AWAKE_SECONDS", 180)
        if isinstance(min_awake_time, int):
            return min_awake_time
        
        ## Assume min_awake_time is a dict
        # If the min_awake_time is a dict, get the value for the current voltage
        try:
            voltage = self.last_voltage
            if voltage is None:
                return abs_min_awake_time
            for threshold, time in sorted(min_awake_time.items()):
                if isinstance(threshold, str):
                    threshold = float(threshold)
                if voltage <= threshold:
                    return time
        except Exception as e:
            logging.warning(f"Error getting min_awake_time: {e}")
        return abs_min_awake_time        

    def override_shutdown_permission_mins(self) -> int:
        default_override_permission_time = 6 * 60
        override_permission_time = self.config.get("OVERRIDE_SHUTDOWN_PERMISSION_MINS", default_override_permission_time)
        if isinstance(override_permission_time, int):
            return override_permission_time
        return default_override_permission_time

    def get_awake_time(self) -> int:
        if self.start_time is None:
            self.start_time = asyncio.get_event_loop().time()
        return int(asyncio.get_event_loop().time() - self.start_time)

    async def maybe_schedule_sleep(self, sleep_time: int, time_till_sleep: int = 20):
        if self.scheduled_goto_sleep_time is not None:
            if self.get_time_till_sleep() is not None:
                logging.warning(f"Time till sleep: {self.get_time_till_sleep()}")
            return

        if self.get_awake_time() < (self.get_min_awake_time() - time_till_sleep):
            time_till_sleep = self.get_min_awake_time() - self.get_awake_time()
            logging.info("Minimum awake time not met: {} seconds to go".format(time_till_sleep))
            return
        
        if not await self.shutdown_permitted() and (self.get_awake_time() < (self.override_shutdown_permission_mins() * 60)):
            logging.info("Scheduling of shutdown not yet permitted by application. Will wait for {} seconds".format(self.override_shutdown_permission_mins() * 60 - self.get_awake_time()))
            return
        
        immunity_time = await self.get_immunity_time()
        if immunity_time is not None:
            logging.info(f"Device immune to shutdown for {immunity_time} seconds.")
            return

        logging.info(f"Scheduling sleep of {sleep_time} secs in {time_till_sleep} secs.")
        self.scheduled_goto_sleep_time = asyncio.get_event_loop().time() + time_till_sleep
        self.scheduled_sleep_time = sleep_time
        await self.run_pre_shutdown_hooks(time_till_sleep, sleep_time)

    def get_time_till_sleep(self):
        if self.scheduled_goto_sleep_time is None:
            return None
        return int(self.scheduled_goto_sleep_time - asyncio.get_event_loop().time())

    def is_ready_to_sleep(self):
        if self.scheduled_goto_sleep_time is None:
            return False
        return asyncio.get_event_loop().time() >= self.scheduled_goto_sleep_time

    async def shutdown_permitted(self):
        for hook in self.request_shutdown_hooks:
            # If the hook is a coroutine, await it
            if asyncio.iscoroutinefunction(hook):
                if not await hook():
                    return False
            else:
                if not hook():
                    return False
        return True
    
    async def get_immunity_time(self):
        immunity_secs = await self.app.platform_iface.get_immunity_seconds_async()
        if immunity_secs is not None and immunity_secs <= 1:
            immunity_secs = None
        return immunity_secs

    async def schedule_next_startup(self):
        if self.scheduled_sleep_time is None:
            self.scheduled_sleep_time = self.get_sleep_time()
        await self.app.platform_iface.schedule_startup_async(self.scheduled_sleep_time)

    async def maybe_reset_soft_watchdog(self):
        ## Continually reset the soft watchdog to 3 hours from now, so that if anything goes wrong, the system will shutdown
        if self.last_watchdog_reset_time is None or asyncio.get_event_loop().time() - self.last_watchdog_reset_time > self.watchdog_reset_interval_secs:
            try:
                await self.app.platform_iface.schedule_shutdown_async(self.soft_watchdog_period_mins * 60)
            except Exception as e:
                logging.error(f"Error scheduling shutdown for soft watchdog: {e}")
            self.last_watchdog_reset_time = asyncio.get_event_loop().time()

    async def assess_power(self):
        """
        Monitor system voltage, determine sleep time, and handle shutdown.
        """
        if not self.is_active():
            return
        
        if self.start_time is None:
            self.start_time = asyncio.get_event_loop().time()

        # Update the system voltage
        await self.update_voltage()

        # If the system is already scheduled to sleep, check if it's time to sleep
        if self.is_ready_to_sleep():
            await self.go_to_sleep()
            return                

        # Determine the sleep time from the config & current voltage
        sleep_time = self.get_sleep_time()
        if sleep_time is None:
            return

        # Attempt to schedule the sleep
        await self.maybe_schedule_sleep(sleep_time)

    async def go_to_sleep(self):
        """
        Put the system to sleep.
        """
        logging.warning("Putting system to sleep...")
        
        ## Run shutdown hooks
        for hook in self.shutdown_hooks:
            await self.run_hook(hook)

        ## schedule the next startup
        await self.schedule_next_startup()

        ## Put the system to sleep
        await self.app.platform_iface.shutdown_async()

        ## Cleanly disconnect the device comms and then wait for sleep
        try:
            self.app.close_app(with_delay=120)
        except Exception as e:
            logging.error(f"Error closing device application for shutdown: {e}")

        ## Wait for the system to shutdown
        time.sleep(120)

    async def run_pre_shutdown_hooks(self, time_till_sleep, sleep_time):
        for hook in self.pre_shutdown_hooks:
            await self.run_hook(
                hook,
                kwargs={
                    "time_till_sleep": time_till_sleep,
                    "sleep_time": sleep_time
                },
            )

    async def run_hook(self, hook, kwargs={}):
        try:
            ## If the hook is a coroutine, await it
            if asyncio.iscoroutinefunction(hook):
                await hook(**kwargs)
            else:
                hook(**kwargs)
        except Exception as e:
            logging.error(f"Error running hook {hook}: {e}")

    async def setup(self):
        logging.info("Setting up PowerManager...")
        await self.maybe_reset_soft_watchdog() ## Set the soft watchdog to 3 hours from now, so that if anything goes wrong, the system will shutdown

        await self.fetch_config()
        if not self.is_active():
            return
        
        ## Attempt 3 times to get a non-None voltage
        for i in range(3):
            if self.last_voltage is None:
                await self.update_voltage()
                await asyncio.sleep(0.1)
            else:
                break

    async def main_loop(self):
        await self.maybe_reset_soft_watchdog()
        await self.assess_power()



# Test Function
if __name__ == "__main__":

    # Simulate the app's interface with required stubs
    class MockPlatformInterface:
        async def get_system_voltage_async(self):
            if not hasattr(self, "start_time"):
                self.start_time = asyncio.get_event_loop().time()
            run_time = asyncio.get_event_loop().time() - self.start_time

            if not hasattr(self, "run_count"):
                self.run_count = 0
            self.run_count += 1

            ## Test Voltages - A steadily decreasing voltage from 13.8 to 11.8 V
            voltage = 13.8 - run_time / 50
            if voltage < 11.8:
                voltage = 11.8

            ## Add a random noise to the voltage (up to 3v)
            import random
            voltage += random.random() * 3
            
            ## Every 5th iteration, simulate a voltage drop
            if self.run_count % 6 < 2:
                voltage -= 5

            ## Every 6th iteration return None
            if self.run_count % 7 < 2:
                voltage = None
            else:
                voltage = round(voltage, 2)

            logging.debug(f"Simulated voltage: {voltage}")
            return voltage

        async def schedule_startup_async(self, sleep_time):
            logging.error(f"Startup scheduled after {sleep_time} seconds.")

        async def schedule_shutdown_async(self, sleep_time):
            logging.error(f"Shutdown scheduled after {sleep_time} seconds.")

        async def get_immunity_seconds_async(self):
            return 0

        async def shutdown_async(self):
            logging.error("System shutting down...")

    class MockApp:
        def __init__(self):
            self.platform_iface = MockPlatformInterface()

        def close_app(self, with_delay=120):
            logging.error("Closing app with delay of {} seconds.".format(with_delay))

        async def get_config_async(self, key_filter=None, wait=True):
            # Simulated configuration for testing
            if key_filter == "POWER_MANAGEMENT":
                return {
                    "VOLTAGE_SLEEP_MINUTES": {
                        12.7: 15,  # 15 mins of sleep if voltage <= 12.7
                        12.2: 60,  # 1 hour of sleep if voltage <= 12.2
                        11.8: 240,   # 4 hours sleep if voltage <= 11.8
                    },
                    # "MIN_AWAKE_SECONDS": 45,  # Minimum awake time in seconds
                    "MIN_AWAKE_SECONDS" : {
                        12.7: 120,
                        12.2: 60,
                        11.8: 40,
                    }
                }
            return {}

    def sync_request_shutdown_hook(**kwargs):
        logging.info("Running synchronous request shutdown hook. {}".format(kwargs))
        return True

    async def async_request_shutdown_hook(**kwargs):
        logging.info("Running asynchronous request shutdown hook. {}".format(kwargs))
        await asyncio.sleep(1)
        return True

    # Define pre-shutdown hooks
    def sync_pre_shutdown_hook(**kwargs):
        logging.info("Running synchronous pre-shutdown hook. {}".format(kwargs))

    async def async_pre_shutdown_hook(**kwargs):
        logging.info("Running asynchronous pre-shutdown hook. {}".format(kwargs))
        await asyncio.sleep(1)

    def sync_shutdown_hook(**kwargs):
        logging.info("Running synchronous shutdown hook. {}".format(kwargs))

    async def async_shutdown_hook(**kwargs):
        logging.info("Running asynchronous shutdown hook. {}".format(kwargs))
        await asyncio.sleep(1)

    # Main testing function
    async def main():
        logging.basicConfig(level=logging.DEBUG)

        # Instantiate the mock app and PowerManager
        app = MockApp()
        power_manager = PowerManager(app)

        # Register request shutdown hooks
        power_manager.register_request_shutdown_hook(sync_request_shutdown_hook)
        power_manager.register_request_shutdown_hook(async_request_shutdown_hook)

        # Register pre-shutdown hooks
        power_manager.register_pre_shutdown_hook(sync_pre_shutdown_hook)
        power_manager.register_pre_shutdown_hook(async_pre_shutdown_hook)

        # Register shutdown hooks
        power_manager.register_shutdown_hook(sync_shutdown_hook)
        power_manager.register_shutdown_hook(async_shutdown_hook)

        # Setup the PowerManager
        await power_manager.setup()

        # Simulate a short monitoring loop for testing
        while True:
            await power_manager.main_loop()
            await asyncio.sleep(2)


    asyncio.run(main())