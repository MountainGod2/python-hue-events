# Python Hue Events

## Description
Python Hue Events is a project that allows users to control their Philips Hue lights in response to updates from the Chaturbate Events API. The application polls events, processes them, and then commands the lights based on these events. (By default, it flashes the lights green when a fan club member joins the room.)

## Installation
To install Python Hue Events, follow these steps:
1. Install Python: [Direct Download Link](https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe)
> [!NOTE]
> Make sure to select ***ADD TO PATH*** during installation.
2. Create an API token: [https://chaturbate.com/statsapi/authtoken/](https://chaturbate.com/statsapi/authtoken/)
> [!NOTE]
> Ensure you select the "Events API" checkbox before creating token.
3. Clone the repository to your local machine and extract it to your documents. [Direct Download Link](https://github.com/MountainGod2/python-hue-events/archive/refs/heads/main.zip)

## Usage
To run the program:
- Open Powershell
  - Navigate to the extracted repository folder. `cd C:\Users\USERNAME\documents\python-hue-events-main`
  - Install the required dependencies. `python -m pip install -r requirements.txt`
  - Run the program and follow the instructions. `python src/main.py`

## Program Logic
The application performs the following tasks:
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

