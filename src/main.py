import asyncio
import logging
import os

import dotenv

from constants import API_TIMEOUT
from event_handler import EventHandler
from event_poller import EventPoller
from hue_bridge import HueBridge
from light_controller import LightController
from log_formatter import LogAligner

# Configure logging to a file
logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Suppress log spam from third-party libraries
logging.getLogger("aiohttp").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("backoff").setLevel(logging.WARNING)
logging.getLogger("qhue").setLevel(logging.WARNING)
logging.getLogger("zeroconf").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


async def main():
    try:
        # Load the environment variables for the username and token
        dotenv.load_dotenv()
        username = os.getenv("USERNAME")
        token = os.getenv("TOKEN")

        # Construct the URL for the Chaturbate Events API
        url = f"https://eventsapi.chaturbate.com/events/{username}/{token}"

    except Exception as e:
        logging.getLogger("Main").error(f"Error loading environment variables: {e}")
        print("Please check the environment variables and try again.")
        return

    try:
        # Initialize the Hue Bridge and Light Controller
        logging.getLogger("Main").debug("Initializing Hue Bridge and Light Controller.")
        hue_bridge = HueBridge()
        light_controller = LightController(hue_bridge)

        logging.getLogger("Main").debug("Initializing Event Handler and Poller.")
        # Initialize the Event Handler
        event_handler = EventHandler()

        # Initialize the Event Poller with the required arguments
        event_poller = EventPoller(url, API_TIMEOUT)

        logging.getLogger("Main").info("Starting program.")
        # Start polling events and processing them
        await event_handler.process_events(event_poller.poll_events(), light_controller)

    except Exception as e:
        logging.getLogger(__name__).exception(e)

    except KeyboardInterrupt:
        logging.getLogger(__name__).info("Exiting due to keyboard interrupt.")

    finally:
        # Align the log entries
        log_aligner = LogAligner(file_path="app.log", delete_original=True)
        await log_aligner.align_log_entries()


if __name__ == "__main__":
    asyncio.run(main())
