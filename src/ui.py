import tkinter as tk

import requests
import apiQueryWrapper
from urllib.request import urlopen
from PIL import Image, ImageTk
from io import BytesIO
from model.player import Player

loaded_user: Player

def load_image_to_canvas(url, canvas):
    print(f"Attempting to load image: {url}")
    try:
        pilimg = Image.open(requests.get(url, stream=True).raw)
        img = ImageTk.PhotoImage(pilimg)

        canvas.create_image(0, 0, anchor=tk.NW, image=img)
        canvas.image = img
    except Exception as e:
        print("Failed to load image: ", e)

def update_user_details(source_widget, canvas_widget=None, label_widget=None):
    print("UpdateUserDetails entered")
    pid = source_widget.get()
    # TODO Format validation to prevent overquerying

    loaded_user = apiQueryWrapper.get_player_data(pid)
    if(loaded_user == None):
        return
    print(f"User {loaded_user.username} Loaded")

    if(canvas_widget != None):
        load_image_to_canvas(loaded_user.avatar, canvas_widget)
    
    if(label_widget != None):
        label_widget.config(text=loaded_user.username)

def create_player_panel(parent):
    #main = tk.Tk(screenName="Player Data")
    panel = tk.Frame(parent, bg="red")

    steamid_input = tk.Entry(panel, width=30)
    steamid_input.pack()

    submit = tk.Button(panel, text="Query for User", command=lambda: update_user_details(steamid_input, canvas_widget=player_img, label_widget=player_label))
    submit.pack()

    player_img = tk.Canvas(panel, width=184, height=184) # Steam avatar resolution
    player_img.pack()

    player_label = tk.Label(panel, name="tempPlayerLabel")
    player_label.pack()

    return panel
    #main.mainloop()

def create_ui():
    # Create the main window
    main = tk.Tk(screenName="Screen Name", baseName="Base Name")

    # Add separate panels
    player_panel = create_player_panel(main)
    player_panel.grid(row=0, column=0)

    # Run window logic and listen for events
    main.mainloop()

create_ui()

# TODO TEMP Roadmap
# Get player data by id input box of some kind
# Game list in a Listbox
# Achievements in a Listbox based on that