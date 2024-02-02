import json
from os import path
import requests
import zeroconf
from qhue import Bridge, QhueException, create_new_username

CREDENTIALS_FILE_PATH = "credentials.json"


class HueBridge:
    def __init__(self):
        self.discovered_ip = None
        self.ip = None
        self.username = None
        self.bridge = None
        self.connect_to_bridge()

    def load_credentials(self):
        if path.exists(CREDENTIALS_FILE_PATH):
            with open(CREDENTIALS_FILE_PATH, "r") as file:
                credentials = json.load(file)
                self.ip = credentials["ip"]
                self.username = credentials["username"]
                return True
        else:
            return False

    def discover_hue_bridge_mdns(self):
        try:
            zeroconf_instance = zeroconf.Zeroconf()
            services = zeroconf_instance.get_service_info(
                "_hue._tcp.local.", "_hue._tcp.local."
            )
            if services:
                self.discovered_ip = services.addresses[0]
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"Error during mDNS discovery: {str(e)}")

    def discover_hue_bridges_cloud(self):
        try:
            response = requests.get("https://discovery.meethue.com/")
            response.raise_for_status()
            data = response.json()
            if data:
                self.discovered_ip = data[0]["internalipaddress"]
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error during cloud discovery: {str(e)}")

    def enter_manual_ip(self):
        try:
            ip = input("Enter the IP address of the Hue bridge: ")
            if ip:
                self.discovered_ip = ip
                return True
            else:
                return False

        except Exception as e:
            raise Exception(f"Error entering manual IP: {str(e)}")

    def find_hue_bridge(self):
        if self.discover_hue_bridge_mdns():
            return self.discovered_ip
        elif self.discover_hue_bridges_cloud():
            return self.discovered_ip
        else:
            return self.enter_manual_ip()

    def create_new_user(self, ip):
        try:
            username = create_new_username(ip)
            return username
        except QhueException as e:
            raise Exception(f"Error creating new user: {str(e)}")

    def save_credentials(self, ip, username):
        credentials = {"ip": ip, "username": username}
        with open(CREDENTIALS_FILE_PATH, "w") as file:
            json.dump(credentials, file)
            return CREDENTIALS_FILE_PATH

    def connect_to_bridge(self):
        if self.load_credentials():
            self.bridge = Bridge(self.ip, self.username)
        else:
            self.ip = self.find_hue_bridge()
            self.username = self.create_new_user(self.ip)
            self.bridge = Bridge(self.ip, self.username)
            self.save_credentials(self.ip, self.username)
