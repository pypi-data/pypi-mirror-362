#!/usr/bin/env python3

import asyncio
import logging
import math
from typing import Optional


class LocationManager:
    def __init__(self, app):
        self.app = app
        self.accuracy_threshold: Optional[float] = None
        self.distance_threshold: Optional[float] = None
        self.location_update_freq_secs: Optional[float] = None
        self.last_published_location = None
        self.last_location_update_time: Optional[float] = None
        self.is_active = False

    async def fetch_config(self):
        config = await self.app.get_config_async(key_filter="LOCATION_MANAGER", wait=True)
        if not config:
            config = {}
            ## Enable LocationManager by default

        if config.get("ENABLED", True) is False:
            logging.info("LocationManager is disabled. Skipping setup.")
            return

        self.accuracy_threshold = config.get("ACCURACY_THRESHOLD", 10)
        self.distance_threshold = config.get("DISTANCE_THRESHOLD", 15)
        self.location_update_freq_secs = config.get("LOCATION_UPDATE_FREQ_SECS", 15)

        if not all(isinstance(value, (int, float)) for value in [
            self.accuracy_threshold, self.distance_threshold, self.location_update_freq_secs
        ]):
            logging.warning("Invalid configuration for LocationManager. Disabling Location Management.")
            self.accuracy_threshold = None
            self.distance_threshold = None
            self.location_update_freq_secs = None
            return

        logging.info(f"LocationManager configured with accuracy_threshold={self.accuracy_threshold}, "
                     f"distance_threshold={self.distance_threshold}, "
                     f"location_update_freq_secs={self.location_update_freq_secs}.")
        self.is_active = True

    async def fetch_location(self) -> Optional[dict]:
        try:
            location = await self.app.platform_iface.get_location_async()
            if not location:
                logging.warning("Failed to fetch location.")
                return None

            ## Transform the location data to a dictionary
            location = {
                "lat": location.latitude,
                "long": location.longitude,
                "alt": location.altitude_m,
                "accuracy": location.accuracy_m,
            }

            logging.debug(f"Fetched location: {location}")
            return location
        except Exception as e:
            logging.error(f"Error fetching location: {e}")
            return None

    def calculate_distance(self, loc1: dict, loc2: dict) -> float:
        """
        Calculate the distance between two locations using the haversine formula.

        :param loc1: First location as a dictionary with 'lat' and 'long'.
        :param loc2: Second location as a dictionary with 'lat' and 'long'.
        :return: Distance in meters.
        """
        R = 6371000  # Earth radius in meters
        lat1, lon1 = math.radians(loc1['lat']), math.radians(loc1['long'])
        lat2, lon2 = math.radians(loc2['lat']), math.radians(loc2['long'])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    async def subscribe_to_location_channel(self):
        self.app.get_agent_iface().add_subscription("location", self.handle_location_channel_update)

    async def handle_location_channel_update(self, channel_name, aggregate):
        logging.debug(f"Received update from {channel_name}: {aggregate}")
        if aggregate and channel_name == "location":
            recv_location = aggregate
            if isinstance(aggregate, str):
                recv_location = {}
                
            self.last_published_location = {
                "lat": recv_location.get("lat", None),
                "long": recv_location.get("long", None),
                "alt": recv_location.get("alt", None),
                "accuracy": recv_location.get("accuracy", None),
            }

    async def publish_location(self, location: dict) -> bool:
        try:
            success = await self.app.get_agent_iface().publish_to_channel_async("location", location)
            return success
        except Exception as e:
            logging.error(f"Error publishing location: {e}")
            return False

    async def setup(self):
        logging.info("Setting up LocationManager...")
        await self.fetch_config()
        if self.is_active:
            await self.subscribe_to_location_channel()

    async def main_loop(self):
        
        if not self.is_active:
            logging.info("LocationManager is inactive. Skipping main loop cycle.")
            return

        current_time = asyncio.get_event_loop().time()

        # Check if the location update frequency interval has passed
        if self.last_location_update_time is not None and \
           (current_time - self.last_location_update_time < self.location_update_freq_secs):
            logging.debug("Location update frequency interval not reached. Skipping.")
            return

        # Update the last location update time
        self.last_location_update_time = current_time

        # Fetch the current location
        location = await self.fetch_location()
        if not location:
            logging.debug("Location is null, skipping update")
            return

        accuracy = location.get("accuracy", float("inf"))
        if accuracy > self.accuracy_threshold:
            logging.debug(f"Location accuracy {accuracy} exceeds threshold {self.accuracy_threshold}. Skipping publish.")
            return

        if self.last_published_location:
            distance = self.calculate_distance(self.last_published_location, location)
            if distance < self.distance_threshold:
                logging.debug(f"Location change ({distance}m) is below threshold {self.distance_threshold}m. Skipping publish.")
                return

        # Publish the new location
        success = await self.publish_location(location)
        if success:
            logging.info(f"Published location: {location}")
            self.last_published_location = location
        else:
            logging.error("Failed to publish location.")