Store Creator is a Python script that automates the process of creating stores in the game Coded Clothing Mall V3 on Roblox. The script uses the Roblox API to buy game passes, claim stores, and create clothing items for each group ID provided by the user.


## Requirements

Python 3.6 or higher
tkinter
requests

## Installation

Clone the repository or download the ZIP file.
Install the required packages by running pip install -r requirements.txt in the terminal.
Run the script by running python store_creator.py in the terminal.


## Usage

Enter the number of stores you want to create in the "Number of Stores" field.
Enter the group IDs you want to use in the "Group IDs" field, separated by commas.
Click the "Start" button to begin creating stores.
Click the "Stop" button to stop creating stores.


## Configuration

The following settings can be configured in the script:
GAME_ID: The ID of the game to create stores in.
GAME_PASS_ID: The ID of the game pass to buy.
SPAWN_LOCATION: The name of the spawn location to use.
NUM_STORES_LIMIT: The maximum number of stores that can be created.
MIN_RATE_LIMIT_DELAY: The minimum delay between requests, in seconds.
MAX_RATE_LIMIT_DELAY: The maximum delay between requests, in seconds.


## Limitations

The script can only create stores in the game Coded Clothing Mall V3 on Roblox.
The script can only create a maximum of 50 stores.
The script is subject to rate limiting by the Roblox API.


## Troubleshooting

If the script is not working, make sure you have entered valid group IDs and that you have bought the game pass for each group.
If the script is being rate limited, try increasing the delay between requests by increasing the MIN_RATE_LIMIT_DELAY and MAX_RATE_LIMIT_DELAY settings.

## Contributing

If you find a bug or have a feature request, please open an issue on GitHub. Pull requests are also welcome.

This project is licensed under the MIT License - see the LICENSE file for details.
