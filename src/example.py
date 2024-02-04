#! /usr/bin/env python3
#
# This prints information about the lights on your hub.
# You'll need to set the IP address of your bridge below.
# It will look for a username for the bridge in a file called
# credentials.json, and if it doesn't find one, it will prompt
# you to create one by pressing the button on the bridge.

import json
from os import path

import yaml
from qhue import Bridge, QhueException, create_new_username

# the IP address of your bridge
BRIDGE_IP = "192.168.0.23"

# the path for the username credentials file
CRED_FILE_PATH = "credentials.json"


def main():
    # check for a credential file
    if not path.exists(CRED_FILE_PATH):
        while True:
            try:
                username = create_new_username(BRIDGE_IP)
                break
            except QhueException as err:
                print("Error occurred while creating a new username: {}".format(err))

        # create a dictionary with the username and any other necessary information
        credentials = {
            "username": username,
            # Add other credentials or information here if needed
        }

        # store the credentials in a JSON file
        with open(CRED_FILE_PATH, "w") as cred_file:
            json.dump(credentials, cred_file, indent=2)
            print("Credentials saved in", CRED_FILE_PATH)

    else:
        print("Reading credentials from", CRED_FILE_PATH)
        with open(CRED_FILE_PATH, "r") as cred_file:
            credentials = json.load(cred_file)
            username = credentials["username"]

    # create the bridge resource, passing the captured username
    bridge = Bridge(BRIDGE_IP, username)

    # print the lights, groups, config, and scenes
    print("Lights:")
    print(yaml.safe_dump(bridge.lights(), indent=4))

    # Uncomment the lines below to print the information

    # print("Groups:")
    # print(yaml.safe_dump(bridge.groups(), indent=4))

    # print("Config:")
    # print(yaml.safe_dump(bridge.config(), indent=4))

    # print("Scenes:")
    # print(yaml.safe_dump(bridge.scenes(), indent=4))


if __name__ == "__main__":
    main()
