import asyncio
import os
from hue_bridge import HueBridge
from light_controller import LightController
from event_handler import EventHandler
from event_poller import EventPoller
import dotenv
import logging


dotenv.load_dotenv(dotenv_path="../.env")

logging.basicConfig(level=logging.DEBUG)


class APIConfig:
    username: str = os.getenv("USERNAME", "")
    token: str = os.getenv("TOKEN", "")
    base_url: str = os.getenv("BASE_URL", "https://eventsapi.chaturbate.com/events")
    request_timeout: int = int(os.getenv("TIMEOUT", "30"))
    url = str(f"{base_url}{username}/{token}?timeout={request_timeout}")


async def main():
    # Load API configuration
    api_config = APIConfig()

    # Initialize the Hue Bridge and Light Controller
    hue_bridge = HueBridge()
    light_controller = LightController(hue_bridge)

    # Initialize the Event Handler
    event_handler = EventHandler()

    # Initialize the Event Poller with the required arguments
    event_poller = EventPoller(api_config.url, api_config.request_timeout)

    # Start polling events and processing them
    await event_handler.process_events(event_poller.poll_events(), light_controller)


if __name__ == "__main__":
    asyncio.run(main())
