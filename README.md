Store Creator

Store Creator is a Python script that creates stores in the Coded Clothing Mall V3 game on Roblox. It allows the user to enter a list of group IDs and the number of stores to create, and automatically creates the stores using clothing from the specified groups.
Getting Started

To use Store Creator, you will need Python 3 installed on your computer. You can download Python 3 from the official website: https://www.python.org/downloads/
You will also need to install the following Python packages:
tkinter
requests
You can install these packages using pip, the Python package installer. Open a command prompt or terminal window and run the following commands:
pip install tkinter
pip install requests

Usage

To use Store Creator, run the script using Python. You can do this by opening a command prompt or terminal window, navigating to the directory where the script is saved, and running the following command:
python store_creator.py

This will launch the Store Creator GUI.
GUI

The Store Creator GUI has the following features:
Start button: Click this button to start creating stores.
Stop button: Click this button to stop creating stores.
Group ID box field: Enter a comma-separated list of group IDs to use for creating stores. You can enter up to 50 group IDs.
Store amount: Enter the number of stores to create. You can enter a number between 1 and 50.
Rate Limiting

Store Creator uses rate limiting to avoid being detected as a bot by Roblox. The delay between requests is set to a random value between 0.5 and 1.5 seconds.
License

This project is licensed under the MIT License - see the LICENSE file for details.
