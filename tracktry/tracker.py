"""
Python wrapper package for the Tracktry API.

This code is released under the terms of the MIT license. See the LICENSE
file for more details.
"""
import asyncio
import logging
import socket
import aiohttp
import async_timeout
from tracktry.const import URL, GOOD_HTTP_CODES

_LOGGER = logging.getLogger(__name__)


class Tracking(object):
    """A class for the Tracktry API."""

    def __init__(self, loop, session, api_key):
        """Initialize the class."""
        self._loop = loop
        self._session = session
        self.api_key = api_key
        self._trackings = {}
        self._couriers = {}
        self._meta = {}
        self.headers = {
            'Tracktry-Api-Key': self.api_key,
            'Content-Type': 'application/json'
        }

    async def get_trackings(self):
        """Get tracking information."""
        self._trackings = {}
        self._meta = {}

        url = "{}/trackings/get".format(URL)
        try:
            async with async_timeout.timeout(8, loop=self._loop):
                response = await self._session.get(url, headers=self.headers)
                result = await response.json()
                try:
                    if response.status in GOOD_HTTP_CODES:
                        self._trackings = result['data']
                    else:
                        _LOGGER.error("Error code %s - %s",
                                      result['meta']['code'],
                                      result['meta']['message'])
                    self._meta = result['meta']
                except (TypeError, KeyError) as error:
                    _LOGGER.error('Error parsing data from Tracktry, %s',
                                  error)
        except (asyncio.TimeoutError,
                aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error('Error connecting to Tracktry, %s', error)
        return self._trackings

    async def add_package_tracking(self, tracking_number, title=None,
                                   slug=None, tracking_postal_code=None):
        """Add tracking information."""
        url = "{}/trackings/post".format(URL)
        data = {
            "tracking_number": tracking_number
        }
        if slug is not None:
            data['carrier_code'] = slug
        if title is not None:
            data['title'] = title
        try:
            async with async_timeout.timeout(8, loop=self._loop):
                await self._session.post(url, headers=self.headers, json=data)
        except (asyncio.TimeoutError,
                aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error('Error connecting to Tracktry, %s', error)

    async def remove_package_tracking(self, slug, tracking_number):
        """Delete tracking information."""
        url = "{}/trackings/{}/{}".format(URL, slug, tracking_number)
        try:
            async with async_timeout.timeout(8, loop=self._loop):
                await self._session.delete(url, headers=self.headers)
        except (asyncio.TimeoutError,
                aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error('Error connecting to Tracktry, %s', error)

    async def detect_couriers_for_tracking_number(self, tracking_number,
                                                  **kwargs):
        """
        Detect couriers for tracking number.

        Add any optional parameters as kwargs when calling the method.
        """
        url = "{}/carriers/detect".format(URL)
        data = {}
        data['tracking_number'] = tracking_number
        couriers = {}
        try:
            async with async_timeout.timeout(8, loop=self._loop):
                response = await self._session.post(url, headers=self.headers,
                                                    json=data)
                result = await response.json()
                try:
                    if response.status in GOOD_HTTP_CODES:
                        couriers = result['data']
                    else:
                        _LOGGER.error("Error code %s - %s",
                                      result['meta']['code'],
                                      result['meta']['message'])
                except (TypeError, KeyError) as error:
                    _LOGGER.error('Error parsing data from Tracktry, %s',
                                  error)
        except (asyncio.TimeoutError,
                aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error('Error connecting to Tracktry, %s', error)
        return couriers

    async def get_couriers(self, **kwargs):
        """
        Get a list of couriers.

        Add any optional parameters as kwargs when calling the method.
        """
        url = "{}/carriers".format(URL)
        couriers = {}
        try:
            async with async_timeout.timeout(8, loop=self._loop):
                response = await self._session.get(url, headers=self.headers)
                result = await response.json()
                try:
                    if response.status in GOOD_HTTP_CODES:
                        self._couriers = result['data']
                    else:
                        _LOGGER.error("Error code %s - %s",
                                      result['meta']['code'],
                                      result['meta']['message'])
                except (TypeError, KeyError) as error:
                    _LOGGER.error('Error parsing data from Tracktry, %s',
                                  error)
        except (asyncio.TimeoutError,
                aiohttp.ClientError, socket.gaierror) as error:
            _LOGGER.error('Error connecting to Tracktry, %s', error)
        return couriers

    @property
    def trackings(self):
        """Return all trackings."""
        return self._trackings

    @property
    def couriers(self):
        """Return all trackings."""
        return self._couriers

    @property
    def meta(self):
        """Return the last meta response."""
        return self._meta
