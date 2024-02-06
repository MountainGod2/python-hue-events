import asyncio
import logging
import os
import re

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


def extract_user_and_token(url):
    """
    Extract the username and token from the Chaturbate API token URL.

    Args:
        url (str): Chaturbate API token URL.

    Returns:
        tuple: Username and token.
    """
    # Extract username and token from the URL using regular expressions
    match = re.match(r"https://eventsapi.chaturbate.com/events/([^/]+)/([^/]+)/", url)
    if match:
        return match.group(1), match.group(2)
    return None, None


def prompt_for_api_url_and_save():
    """
    Prompt the user for the Chaturbate API token URL and save the username and token to the .env file.

    Returns:
        tuple: Username and token.
    """
    while True:
        api_url = input("Enter your Chaturbate API token URL: ")
        username, token = extract_user_and_token(api_url)
        if username and token:
            # Save the username and token to the .env file
            with open(".env", "a") as env_file:
                env_file.write(f"USERNAME={username}\n")
                env_file.write(f"TOKEN={token}\n")
            return username, token
        else:
            print("Invalid URL format. Please enter a valid Chaturbate API token URL.")


async def main():
    """
    Main function to start the program.
    """
    try:
        # Load the environment variables for the username and token
        dotenv.load_dotenv()
        user = os.getenv("USERNAME")
        token = os.getenv("TOKEN")

        # Check if username and token are set, and if not, prompt the user for the API token URL
        if not user or not token:
            user, token = prompt_for_api_url_and_save()

        # Construct the URL for the Chaturbate Events API
        url = f"https://eventsapi.chaturbate.com/events/{user}/{token}"

    except Exception as e:
        logging.getLogger("Main").error(f"Error loading environment variables: {e}")
        print("Please check the environment variables and try again.")
        return

    try:
        # Initialize the Hue Bridge and Light Controller
        logging.getLogger("Main").debug("Initializing Hue Bridge and Light Controller.")
        hue = HueBridge()
        light_ctrl = LightController(hue)

        logging.getLogger("Main").debug("Initializing Event Handler and Poller.")
        # Initialize the Event Handler
        event_handler = EventHandler()

        # Initialize the Event Poller with the required arguments
        event_poller = EventPoller(url, API_TIMEOUT)

        logging.getLogger("Main").info("Starting program.")
        print("Starting program.")

        # Start polling events and processing them
        await event_handler.process_events(event_poller.poll_events(), light_ctrl)

    except Exception as e:
        logging.getLogger(__name__).exception(e)

    except KeyboardInterrupt:
        logging.getLogger(__name__).info("Exiting due to keyboard interrupt.")

    finally:
        logging.getLogger("Main").info("Shutting down.")
        # Align the log entries
        log_aligner = LogAligner(file_path="app.log", delete_original=False)
        await log_aligner.align_log_entries()


if __name__ == "__main__":
    asyncio.run(main())
