"""Constants for the alert light program."""
import os
from dataclasses import dataclass

import dotenv

dotenv.load_dotenv()


@dataclass
class APIConfig:
    username: str = os.getenv("USERNAME", "")
    token: str = os.getenv("TOKEN", "")
    base_url: str = os.getenv("BASE_URL", "https://eventsapi.chaturbate.com/events/")
    request_timeout: int = int(os.getenv("TIMEOUT", "30"))


# Other parameters
MAX_RETRY_DELAY = 60  # Maximum delay between retries in seconds
RETRY_FACTOR = 2  # Factor by which to increase retry delay
INITIAL_RETRY_DELAY = 5  # Initial delay between retries in seconds
SECONDS_PER_MIN = 60  # Number of seconds in a minute
API_TIMEOUT = 2  # Timeout for API requests in seconds
