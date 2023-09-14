import time
import requests
import random
import logging
import sys

# Game settings
GAME_ID = 7406897155
GAME_PASS_ID = 24229952 
SPAWN_LOCATION = "SpawnLocation"

# Configurable settings
NUM_STORES_LIMIT = 50
MIN_RATE_LIMIT_DELAY = 3
MAX_RATE_LIMIT_DELAY = 48

done_groups = []

def main():
    group_ids = input("Enter group IDs (separated by commas): ")
    group_ids = [int(x) for x in group_ids.split(",")]

    num_stores = int(input("Enter number of stores to create: "))

    if num_stores > len(group_ids):
        num_stores = len(group_ids)

    for i in range(num_stores):
        group_id = group_ids[i]
        if group_id in done_groups:
            continue

        player = get_player_for_group(group_id)

        if not has_gamepass(player):
            buy_gamepass(player)

        claim_store(player)
        create_store()

        done_groups.append(group_id)

        time.sleep(random.randint(MIN_RATE_LIMIT_DELAY, MAX_RATE_LIMIT_DELAY))

def get_player_for_group(group_id):
    response = requests.get(f"https://groups.roblox.com/v1/groups/{group_id}/roles")
    roles = response.json()["roles"]
    for role in roles:
        if role["name"] == "Owner":
            owner_id = role["user"]["id"]
            break

    response = requests.get(f"https://api.roblox.com/users/{owner_id}/username")
    username = response.text

    return username

def has_gamepass(player):
    response = requests.get(f"https://inventory.roblox.com/v1/users/{player}/items/GamePass/{GAME_PASS_ID}")
    return response.json()["data"] != []

def buy_gamepass(player):
    response = requests.post(f"https://economy.roblox.com/v1/purchases/products/{GAME_PASS_ID}", json={"expectedCurrency":1}, cookies={"GuestData":""})
    if response.status_code == 200:
        logging.info(f"Bought gamepass for {player}")
    else:
        logging.error(f"Failed to buy gamepass for {player}")

def claim_store(player):
    response = requests.post(f"https://games.roblox.com/v1/games/{GAME_ID}/servers/Public?limit=100")
    servers = response.json()["data"]
    random.shuffle(servers)
    for server in servers:
        response = requests.get(f"https://games.roblox.com/v1/games/{GAME_ID}/servers/Public?serverIds={server['id']}")
        server_data = response.json()["data"][0]
        if server_data["maxPlayers"] == server_data["playing"] and server_data["reserved"] == 0:
            continue

        response = requests.post(f"https://games.roblox.com/v1/games/{GAME_ID}/servers/{server['id']}/join", json={"player":{"name":player}}, headers={"Referer":f"https://www.roblox.com/games/{GAME_ID}/"})
        if response.status_code == 200:
            logging.info(f"Joined server {server['id']} for {player}")
            break

    character = None
    while not character:
        try:
            response = requests.get(f"https://users.roblox.com/v1/users/get-by-username?username={player}")
            user_id = response.json()["id"]
            response = requests.get(f"https://avatar.roblox.com/v1/users/{user_id}/currently-wearing")
            character = response.json()["assetIds"]
        except:
            time.sleep(1)

    store = None
    while not store:
        for obj in requests.get(f"https://avatar.roblox.com/v1/users/{user_id}/inventory/3?assetTypeId=41").json()["data"]:
            if obj["name"].startswith("Store #"):
                store = obj["id"]
                break

        if not store:
            time.sleep(1)

    response = requests.post(f"https://avatar.roblox.com/v1/avatar/set-wearing-assets", json={"assetIds":character + [store]}, headers={"Referer":f"https://www.roblox.com/games/{GAME_ID}/"})
    if response.status_code == 200:
        logging.info(f"Claimed store for {player}")
    else:
        logging.error(f"Failed to claim store for {player}")

    response = requests.post(f"https://games.roblox.com/v1/games/{GAME_ID}/servers/{server['id']}/leave", headers={"Referer":f"https://www.roblox.com/games/{GAME_ID}/"})
    if response.status_code == 200:
        logging.info(f"Left server {server['id']} for {player}")
    else:
        logging.error(f"Failed to leave server {server['id']} for {player}")

def create_store():
    response = requests.post(f"https://avatar.roblox.com/v1/groups/{GAME_PASS_ID}/store")
    if response.status_code == 200:
        logging.info("Created store")
    else:
        logging.error("Failed to create store")

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    main()
