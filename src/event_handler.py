import logging


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
            light_controller (LightController): Light controller instance.
        """
        async for events in events_gen:
            for event in events:
                try:
                    event_method = event["method"]
                    self.logger.debug(f"Received event: {event_method}")
                    if event_method == "userEnter":
                        await self.process_user_enter(
                            event, light_controller
                        )  # Await the async method

                except KeyError as e:
                    self.logger.error(f"Key error in event data: {e}")

    async def process_user_enter(self, event_dict, light_controller):
        """
        Process user enter event.

        Args:
            event_dict (dict): Event data.
            light_controller (LightController): Light controller instance.
        """
        try:
            self.logger.info("User entered the room.")
            user_data = event_dict.get("object", {}).get("user", {})
            username = user_data.get("username", "Unknown")
            in_fanclub = user_data.get("inFanclub", False)

            self.logger.debug(f"User entered: {username}, In Fan Club: {in_fanclub}")

            if in_fanclub:
                light_controller.flash_group_lights(0)

            else:
                self.logger.debug("User is not in the fan club. Ignoring.")

        except Exception as e:
            self.logger.error(f"Error processing user enter event: {e}")
