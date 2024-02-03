import asyncio
import os
from hue_bridge import HueBridge
from light_controller import LightController
from event_handler import EventHandler
from event_poller import EventPoller
import dotenv
import logging


logging.basicConfig(level=logging.DEBUG)


async def main():
    dotenv.load_dotenv()
    url = os.getenv("API_URL")

    # Initialize the Hue Bridge and Light Controller
    hue_bridge = HueBridge()
    light_controller = LightController(hue_bridge)

    # Initialize the Event Handler
    event_handler = EventHandler()

    # Initialize the Event Poller with the required arguments
    event_poller = EventPoller(url, 20)

    # Start polling events and processing them
    await event_handler.process_events(event_poller.poll_events(), light_controller)


if __name__ == "__main__":
    asyncio.run(main())
