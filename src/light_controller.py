import json
import time
import yaml


class LightController:
    def __init__(self, bridge):
        self.bridge = None

    def list_lights(self):
        lights = self.bridge.lights()
        for light_id, light in lights.items():
            print(f"{light_id}: {light['name']}")
        return lights

    def list_light_details(self, light_id, format="json"):
        light = self.bridge.lights[light_id]()
        if format == "json":
            print(json.dumps(light["state"], indent=2))
        elif format == "yaml":
            print(yaml.safe_dump(light["state"], indent=4))
        else:
            print("Invalid format specified.")
        return light["state"]

    def get_light_state(self, light_id):
        light = self.bridge.lights[light_id]()
        state = light["state"]["on"]
        print(f"Light {light_id} is {'on' if state else 'off'}")
        return state

    def flash_light(self, light_id):
        light = self.bridge.lights[light_id]()

        # Save current state
        state = light["state"]["on"]

        # Get current state
        xy = light["state"]["xy"]
        bri = light["state"]["bri"]
        print(f"Current xy: {xy}")
        print(f"Current brightness: {bri}")

        # Flash green
        print(f"Flashing light(s): {light_id} green")

        self.bridge.lights(light_id, "state", on=True, bri=200, xy=[0.1, 0.8])
        time.sleep(1)
        self.bridge.lights(light_id, "state", on=False)
        time.sleep(1)
        self.bridge.lights(light_id, "state", on=True, bri=200, xy=[0.1, 0.8])
        time.sleep(1)
        self.bridge.lights(light_id, "state", on=False)
        time.sleep(1)

        # Restore previous state
        print(f"Restoring previous state for light(s): {light_id}")
        self.bridge.lights(light_id, "state", on=state, bri=bri, xy=xy)
