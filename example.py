"""Example usage of tracktry."""
import asyncio
import aiohttp
from tracktry.tracker import Tracking

API_KEY = 'API_KEY_HERE'


async def example():
    """Get pending packages."""
    async with aiohttp.ClientSession() as session:
        tracktry = Tracking(LOOP, session, API_KEY)
        packages = await tracktry.get_trackings()
        print("Pending packages:", packages)


async def detect_couriers_example():
    """Detect couriers for tracking number."""
    async with aiohttp.ClientSession() as session:
        tracktry = Tracking(LOOP, session, API_KEY)
        tracking_number = "1Z9999999999999999"
        couriers = await tracktry.detect_couriers_for_tracking_number(
            tracking_number
        )
        print("Possible couriers:", couriers)


LOOP = asyncio.get_event_loop()
LOOP.run_until_complete(example())
LOOP.run_until_complete(detect_couriers_example())
