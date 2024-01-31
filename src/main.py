import argparse
import zeroconf
import requests
import json
import time

import yaml
from os import path
from qhue import Bridge, QhueException, create_new_username


class HueIPConfigurator:
    CREDENTIALS_FILE_PATH = "credentials.json"

    def __init__(self):
        self.discovered_ip = None
        self.credentials = None

    def create_new_username(self):
        max_retries = 3
        for retry in range(max_retries):
            try:
                username = create_new_username(self.discovered_ip)
                self.credentials = username
                break
            except QhueException as err:
                print(f"Error occurred while creating a new username: {err}")
                if retry < max_retries - 1:
                    print(f"Retrying ({retry + 2}/{max_retries})...")
                else:
                    print("Max retries reached. Exiting.")
                    return

    def load_data_from_file(self):
        try:
            with open(self.CREDENTIALS_FILE_PATH, "r") as file:
                data = json.load(file)
                self.discovered_ip = data.get("ip_address")
                self.credentials = data.get("username")
        except Exception:
            print("No data found in file. Continuing to configure bridge.")

    def discover_hue_bridge_mdns(self):
        try:
            zeroconf_instance = zeroconf.Zeroconf()
            services = zeroconf_instance.get_service_info(
                "_hue._tcp.local.", "_hue._tcp.local."
            )
            if services:
                self.discovered_ip = services.addresses[0]
                print("Hue Bridge found via mDNS:")
                print(f"IP Address: {self.discovered_ip}")
                print(f"Bridge ID: {services.server.split('.')[0]}")
                return True
            else:
                print("Hue Bridge not found via mDNS.")
                return False
        except Exception as e:
            print(f"Error during mDNS discovery: {str(e)}")
            return False

    def discover_hue_bridges_cloud(self):
        if not self.discovered_ip:
            url = "https://discovery.meethue.com"
            try:
                response = requests.get(url)
                response.raise_for_status()
                bridges = response.json()
                if bridges:
                    self.discovered_ip = bridges[0].get("internalipaddress")
                    print("Hue Bridge found via cloud:")
                    print(f"IP Address: {self.discovered_ip}")
                    print(f"Bridge ID: {bridges[0].get('id')}")
                    return True
                else:
                    print("No bridges found via cloud.")
                    return False
            except requests.exceptions.RequestException as e:
                print(f"Error during cloud discovery: {str(e)}")
                return False
            except json.JSONDecodeError as e:
                print(f"Error decoding cloud discovery response: {str(e)}")
                return False
        return True

    def manual_ip_entry(self):
        manual_ip = input(
            "Enter the IP address of the Hue bridge (or leave blank to skip): "
        )
        if manual_ip:
            self.discovered_ip = manual_ip
            return True
        else:
            return False

    def check_bridge_configuration(self):
        if self.discovered_ip:
            url = f"http://{self.discovered_ip}/api/0/config"
            try:
                response = requests.get(url)
                response.raise_for_status()
                if response.status_code == 200:
                    return True
                else:
                    print(
                        f"Bridge configuration check failed. Status code: {response.status_code}"
                    )
                    return False
            except requests.exceptions.RequestException as e:
                print(f"Error during bridge configuration check: {str(e)}")
                return False
            except json.JSONDecodeError as e:
                print(f"Error decoding bridge configuration response: {str(e)}")
                return False
        else:
            print("No IP address found. Cannot check bridge configuration.")
            return False

    def save_data_to_file(self):
        data = {}
        if self.discovered_ip:
            data["ip_address"] = self.discovered_ip
        if self.credentials:
            data["username"] = self.credentials

        if data:
            existing_data = {}
            if path.exists(self.CREDENTIALS_FILE_PATH):
                try:
                    with open(self.CREDENTIALS_FILE_PATH, "r") as file:
                        existing_data = json.load(file)
                except Exception as e:
                    print(f"Error while reading existing data from file: {str(e)}")

            for key, value in data.items():
                if key not in existing_data or existing_data[key] != value:
                    existing_data[key] = value

            try:
                with open(self.CREDENTIALS_FILE_PATH, "w") as file:
                    json.dump(existing_data, file)
            except Exception as e:
                print(f"Error while saving data to file: {str(e)}")
        else:
            print("No data to save. Skipping save to file.")

    def configure_bridge(self):
        self.load_data_from_file()

        if self.discovered_ip and self.credentials:
            return

        if not self.discovered_ip:
            if self.discover_hue_bridge_mdns():
                return

            if self.discover_hue_bridges_cloud():
                return

            if self.manual_ip_entry():
                return

            print("No IP address found. Exiting.")
            return


class HueLightController:
    @staticmethod
    def flash_light(bridge, light_id):
        light = bridge.lights[light_id]()

        # Check if light is on
        light_on = light["state"]["on"]

        # Get current state
        xy = light["state"]["xy"]
        bri = light["state"]["bri"]
        print(f"Current xy: {xy}")
        print(f"Current brightness: {bri}")

        # Flash green
        print(f"Flashing light(s): {light_id} green")

        bridge.lights(light_id, "state", on=True, bri=200, xy=[0.1, 0.8])
        time.sleep(1)
        bridge.lights(light_id, "state", on=False)
        time.sleep(1)
        bridge.lights(light_id, "state", on=True, bri=200, xy=[0.1, 0.8])
        time.sleep(1)
        bridge.lights(light_id, "state", on=False)
        time.sleep(1)

        # Restore previous state
        print(f"Restoring previous state for light(s): {light_id}")
        bridge.lights(light_id, "state", on=light_on, bri=bri, xy=xy)

    @staticmethod
    def list_lights(bridge):
        lights = bridge.lights()
        for light_id, light in lights.items():
            print(f"{light_id}: {light['name']}")

    @staticmethod
    def list_light_details(bridge, light_id, format="json"):
        light = bridge.lights[light_id]()
        if format == "json":
            print(json.dumps(light["state"], indent=2))
        elif format == "yaml":
            print(yaml.safe_dump(light["state"], indent=4))
        else:
            print("Invalid format specified.")

    @staticmethod
    def get_light_state(bridge, light_id):
        light = bridge.lights[light_id]()
        state = light["state"]["on"]
        print(f"Light {light_id} is {'on' if state else 'off'}")


def perform_setup():
    configurator = HueIPConfigurator()
    configurator.configure_bridge()

    if not configurator.discovered_ip:
        print("No IP address found. Exiting setup.")
        return

    if not configurator.check_bridge_configuration():
        return

    configurator.create_new_username()
    if not configurator.credentials:
        print("No credentials found. Exiting setup.")
        return
    else:
        configurator.save_data_to_file()
        print("Setup completed successfully.")


def main():
    parser = argparse.ArgumentParser(description="Hue Light Controller")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--setup", action="store_true", help="Perform initial setup (IP and username)"
    )
    group.add_argument("--flash", metavar="light_id", type=int, help="Flash a light")
    group.add_argument("--list-lights", action="store_true", help="List all lights")
    group.add_argument(
        "--list-details", metavar="light_id", type=int, help="List light details"
    )
    group.add_argument(
        "--format",
        choices=["json", "yaml"],
        default="json",
        help="Output format for light details",
    )
    group.add_argument(
        "--get-state", metavar="light_id", type=int, help="Get light state"
    )

    args = parser.parse_args()

    if args.setup:
        perform_setup()
        return

    if not path.exists(HueIPConfigurator.CREDENTIALS_FILE_PATH):
        print("You need to run the setup (--setup) before using other commands.")
        return

    configurator = HueIPConfigurator()
    configurator.load_data_from_file()
    bridge = Bridge(configurator.discovered_ip, configurator.credentials)

    if args.flash is not None:
        HueLightController.flash_light(bridge, args.flash)
    elif args.list_lights:
        HueLightController.list_lights(bridge)
    elif args.list_details is not None:
        HueLightController.list_light_details(bridge, args.list_details, args.format)
    elif args.get_state is not None:
        HueLightController.get_light_state(bridge, args.get_state)


if __name__ == "__main__":
    main()
