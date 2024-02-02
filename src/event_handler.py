from pydantic import BaseModel, ValidationError
import logging


# Define Pydantic models for structured data
class User(BaseModel):
    username: str = "Unknown"


class EventHandler:
    """
    Class to process events.

    Attributes:
        logger (logging.Logger): Logger instance.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    async def process_events(self, events_gen, light_controller):
        """
        Process events.

        Args:
            events_gen (generator): Generator for events.
        """
        async for events in events_gen:
            for event in events:
                try:
                    event_method = event["method"]
                    self.logger.debug(f"Received event: {event_method}")
                    if event_method == "userEnter":
                        self.process_user_enter(event, light_controller)

                except KeyError as e:
                    self.logger.error(f"Key error in event data: {e}")

        async def process_user_enter(self, event_dict, light_controller):
            try:
                self.logger.info("User entered the room.")
                user_data = event_dict.get("object", {})
                user = User(**user_data)
                username = user.username
                self.logger.debug(f"User entered: {username}")
                light_controller.flash_light(5)

            except ValidationError as e:
                self.logger.error(f"Validation error: {e}")
                for error in e.errors():
                    self.logger.error(
                        f"Error in field '{error['loc'][0]}': {error['msg']}"
                    )

            except Exception as e:
                self.logger.error(f"Error processing user enter event: {e}")
