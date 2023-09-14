import tkinter as tk
import tkinter.messagebox as messagebox
import time
import requests
import random
import logging
import sys
import threading

# Game settings
GAME_ID = 7406897155
GAME_PASS_ID = 24229952 
SPAWN_LOCATION = "SpawnLocation"

# Configurable settings
NUM_STORES_LIMIT = 50
MIN_RATE_LIMIT_DELAY = 3
MAX_RATE_LIMIT_DELAY = 48

done_groups = []

root = tk.Tk()
root.title("Store Creator")
root.geometry("400x300")

def start_creating():
  
  num_stores, group_ids = validate_input()
  
  if num_stores and group_ids:
    global stop_event
    stop_event = threading.Event()
    start_button.config(state="disabled")
    stop_button.config(state="normal")
    threading.Thread(target=create_stores, args=(num_stores, group_ids)).start()

# Create GUI
num_stores_label = tk.Label(root, text="Number of Stores:")
num_stores_entry = tk.Entry(root)

group_ids_label = tk.Label(root, text="Group IDs (separated by commas):")
group_ids_entry = tk.Entry(root) 

start_button = tk.Button(root, text="Start", command=start_creating)
stop_button = tk.Button(root, text="Stop", command=stop_creating, state="disabled")

# Layout GUI elements 
num_stores_label.pack()
num_stores_entry.pack()

group_ids_label.pack()
group_ids_entry.pack()

start_button.pack(pady=20)
stop_button.pack(pady=10)

# Background gradient
canvas = tk.Canvas(root, width=400, height=300)
canvas.pack()

for i in range(400):
  canvas.create_line(0, i, 600, i, fill=f"#{i:02x}00ff")

def validate_input():
  # Validate input
  num_stores = int(num_stores_entry.get())
  group_ids = group_ids_entry.get()
  
  if not isinstance(num_stores, int) or num_stores < 1 or num_stores > NUM_STORES_LIMIT:
    messagebox.showerror("Invalid input", "Number of stores must be between 1 and {}".format(NUM_STORES_LIMIT))
    return  

  try:
    group_ids = [int(x) for x in group_ids.split(",")]
  except ValueError:
    messagebox.showerror("Invalid input", "Group IDs must be integers")
    return

  return num_stores, group_ids

def claim_store(player):

  # Join game
  response = requests.post("http://localhost:6463/game/join?placeId={}&playerName={}&spawnLocationName={}&spawnLocationType=CFrame".format(GAME_ID, player, SPAWN_LOCATION))

  # Get player's character
  character = None
  while not character:
    try:
      character = requests.get("http://localhost:6463/game/getplayercharacter?playerName={}".format(player)).json()["character"] 
    except:
      time.sleep(1)

  # Find available store
  store = None
  while not store:
    for obj in requests.get("http://localhost:6463/game/getallchildren?parentId={}&classname=Model&name=Store".format(character)).json():
      store = obj["id"]
      break
      
    if not store:
      time.sleep(1)

  # Press E to claim store
  requests.post("http://localhost:6463/game/sendkey?playerName={}&keyCode=Enum.KeyCode.E&isKeyDown=true".format(player))
  requests.post("http://localhost:6463/game/sendkey?playerName={}&keyCode=Enum.KeyCode.E&isKeyDown=false".format(player))

  # Leave game
  requests.post("http://localhost:6463/game/leavegame?playerName={}".format(player))
  
def create_stores(num_stores, group_ids):

  for group_id in group_ids:
  
    if group_id in done_groups:
      continue
      
    # Get player info
    player = get_player_for_group(group_id)
    
    # Claim store
    claim_store(player)

    # Create store
    create_store()

    done_groups.append(group_id)
    
    # Random rate limit delay
    time.sleep(random.randint(MIN_RATE_LIMIT_DELAY, MAX_RATE_LIMIT_DELAY))
    
def stop_creating():
  global stop_event
  stop_event.set()
  start_button.config(state="normal")
  stop_button.config(state="disabled")

root.mainloop()
