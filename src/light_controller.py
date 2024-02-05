import json
import logging
import time

import yaml


class LightController:
    """
    Class to control Hue lights.

    Attributes:
        bridge (HueBridge): Hue bridge instance.
        logger (logging.Logger): Logger instance.
    """

    def __init__(self, bridge):
        self.bridge = bridge
        self.logger = logging.getLogger(self.__class__.__name__)

    def list_lights(self):
        """
        List lights.

        Returns:
            dict: Dictionary of lights.
        """
        lights = self.bridge.bridge.lights()
        for light_id, light in lights.items():
            self.logger.info(f"Light {light_id}: {light['name']}")
        return lights

    def list_light_details(self, light_id, format="json"):
        """
        List light details.

        Args:
            light_id (str): Light ID.
            format (str): Output format. Defaults to "json".

        Returns:
            dict: Dictionary of light details.
        """
        light = self.bridge.bridge.lights[light_id]()
        if format == "json":
            self.logger.info(json.dumps(light["state"], indent=4))
        elif format == "yaml":
            self.logger.info(yaml.safe_dump(light["state"], indent=4))
        else:
            self.logger.error(f"Invalid format: {format}")
        return light["state"]

    def get_light_state(self, light_id):
        """
        Get light state.

        Args:
            light_id (str): Light ID.

        Returns:
            bool: True if light is on, False if light is off.
        """
        light = self.bridge.bridge.lights[light_id]()
        state = light["state"]["on"]
        self.logger.info(f"Light {light_id} is {'on' if state else 'off'}")
        return state

    def flash_group_lights(self, group_id):
        """
        Flash group lights.

        Args:
            group_id (str): Group ID.
        """

        # Flash green
        self.logger.info("Flashing lights green")

        self.bridge.bridge.groups(group_id, "action", on=True, bri=200, xy=[0.1, 0.8])
        time.sleep(0.6)
        self.bridge.bridge.groups(group_id, "action", on=False)
        time.sleep(1)
        self.bridge.bridge.groups(group_id, "action", on=True, bri=200, xy=[0.1, 0.8])
        time.sleep(0.6)
        self.bridge.bridge.groups(group_id, "action", on=False)
        time.sleep(1)

        self.logger.info("Returning lights to neutral color")
        self.bridge.bridge.groups(
            group_id, "action", on=True, bri=254, xy=[0.413, 0.395]
        )
