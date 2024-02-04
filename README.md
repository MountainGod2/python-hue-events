# Python Hue Events

## Description
Python Hue Events is a project that allows users to control their Philips Hue lights in response to updates from the Chaturbate Events API. The application polls events, processes them, and then commands the lights based on these events. (By default, it flashes the lights green when a fan club member joins the room.)

## Prerequisites

- Python 3.x: [Download Python](https://www.python.org/downloads/)
- Libraries: See `requirements.txt`

## Installation
To install Python Hue Events, follow these steps:
1. Clone the repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt` in your terminal.
3. Create an API token: `https://chaturbate.com/statsapi/authtoken/` (Ensure you select the "Events API" checkbox).
4. Follow the program instructions to setup your .env file and Hue credentials.

## Usage
After installation, you can run the project by executing the `main.py` script in the `src` directory. The application performs the following tasks:
- Initializes the connection with the Philips Hue Bridge.
- Sets up light control mechanisms.
- Polls the Chaturbate Events API for updates.
- Handles the received events to control the lighting based on predefined logic.

## Files and Functionality
- `main.py`: Initializes the application, sets up logging, loads environment variables, and runs the main event loop.
- `hue_bridge.py`: Manages communication with the Philips Hue Bridge, including light control commands.
- `light_controller.py`: Integrates with `hue_bridge.py` to control the behavior of the lights.
- `event_handler.py`: Processes the events received from the polling mechanism and decides the light behavior.
- `event_poller.py`: Continuously polls the Chaturbate Events API and manages error handling with retry mechanisms.

## Contributing
Contributions are welcome. Feel free to fork the repository, make changes, and submit a pull request.

## License
This project is licensed under the MIT License.

