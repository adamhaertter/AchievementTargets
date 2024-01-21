import tkinter as tk
from tkinter import ttk

import requests
import apiQueryWrapper
from urllib.request import urlopen
from PIL import Image, ImageTk
from io import BytesIO
from model.player import Player
from model.game import Game
from model.achievement import Achievement

loaded_user: Player
loaded_library: list[Game] = []
loaded_all_achievements: list[Achievement] = []

# Able to resize image if specific dimensions are passed in, otherwise uses default dimensions
def load_image_to_canvas(url, canvas, width=0, height=0):
    print(f"Attempting to load image: {url}")
    try:
        pilimg = Image.open(requests.get(url, stream=True).raw)

        if(width != 0 and height != 0):
            pilimg = pilimg.resize((width, height), Image.Resampling.NEAREST) # LANCZOS for antialias, but crunches pixel games
        
        img = ImageTk.PhotoImage(pilimg)

        canvas.create_image(0, 0, anchor=tk.NW, image=img)
        canvas.image = img
    except Exception as e:
        print("Failed to load image: ", e)

def update_user_details(source_widget, canvas_widget=None, label_widget=None):
    global loaded_user
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

def update_games_list(listbox:tk.Listbox):
    global loaded_library

    library = apiQueryWrapper.get_owned_games(loaded_user.player_id)
    loaded_library = sorted(library, key=lambda game: game.title)

    # Clear current list
    listbox.delete(0, tk.END)

    maxlength = 0
    for item in loaded_library:
        listbox.insert(tk.END, item)
        if(len(item.title) > maxlength):
            maxlength = len(item.title)

    listbox.config(width=maxlength)

def create_games_panel(parent):
    panel = tk.Frame(parent, bg="green")

    global games_list
    games_list = tk.Listbox(panel, selectmode=tk.SINGLE)
    games_list.pack()

    fetch = tk.Button(panel, text="Fetch Library", command=lambda:update_games_list(games_list))
    fetch.pack()

    return panel

def get_selected_item(listbox:tk.Listbox, iterable:list):
    selected = listbox.curselection()
    if selected:
        #selected = listbox.get(selected)
        selected = iterable[int(selected[0])]
        print(f"Selected Item: {selected}")
        return selected
    else:
        print("No item selected at this time")
        return None

def update_achievements_list(listbox:tk.Listbox, canvas:tk.Canvas = None):
    loaded_game = get_selected_item(games_list, loaded_library)
    if(loaded_game == None):
        return
    
    global loaded_all_achievements
    loaded_all_achievements = apiQueryWrapper.get_game_achievements(loaded_game.game_id)
    loaded_owned_achievements = apiQueryWrapper.get_player_achievements(loaded_user.player_id, loaded_game.game_id)

    # Update all achieved bool to be accurate
    tuple_dict = dict(loaded_owned_achievements)
    for target in loaded_all_achievements:
        if target.achievement_id in tuple_dict:
            target.achieved = tuple_dict[target.achievement_id]

    # Clear out old data
    listbox.delete(0, tk.END)

    for item in loaded_all_achievements:
        listbox.insert(tk.END, item)
    listbox.config(width=100)
    
    if(canvas != None):
        load_image_to_canvas(loaded_game.get_preview_art(), canvas)

def create_achievement_panel(parent):
    panel = tk.Frame(parent, bg="blue")

    game_art_img = tk.Canvas(panel, width=184, height=69) # Steam preview capsule regulated size
    game_art_img.pack()

    global achievement_list
    achievement_list = tk.Listbox(panel)
    achievement_list.pack()

    fetch = tk.Button(panel, text="Refresh Achievements", command=lambda:update_achievements_list(achievement_list, game_art_img))
    fetch.pack()

    show_popup = tk.Button(panel, text="Expand Popup", command=lambda:achievement_detail_popup(parent))
    show_popup.pack()

    return panel

def achievement_detail_popup(parent):
    wrap_length = 250
    display_font = "Segoe UI"
    background_color = "#121212"
    text_color = "#ffffff"

    popup = tk.Toplevel(parent)
    popup.title = "Achievement Details"
    popup.config(bg=background_color)

    target_label = tk.Label(popup, font=(display_font, 20, "bold"))
    target_label.config(text="Current Target", fg="red", background=background_color)
    target_label.grid(row=0, column=0)

    content_panel = tk.Frame(popup)
    content_panel.grid(row=1, column=0)
    content_panel.configure(background=background_color)

    loaded_achievement : Achievement = get_selected_item(achievement_list, loaded_all_achievements)

    icon_art = tk.Canvas(content_panel, width=128, height=128)
    icon_art.grid(row=0, column=0, padx=5, pady=5)
    icon_art.config(background=background_color)
    #icon_art.pack()
    load_image_to_canvas(loaded_achievement.icon, icon_art, width=128, height=128)

    labels_panel = tk.Frame(content_panel, width=wrap_length)
    labels_panel.columnconfigure(0, minsize=wrap_length)
    labels_panel.config(background=background_color)

    title_text = ttk.Label(labels_panel, font=(display_font, 16, 'bold'), wraplength=wrap_length)
    title_text.config(text=loaded_achievement.name, foreground=text_color, background=background_color)
    title_text.grid(row=0, column=0)
    #title_text.pack()

    desc_text = ttk.Label(labels_panel, font=(display_font, 12), wraplength=wrap_length)
    desc_text.config(text=loaded_achievement.desc, foreground=text_color, background=background_color)
    desc_text.grid(row=1, column=0)
    #desc_text.pack()

    
    labels_panel.grid(row=0, column=1)
    #labels_panel.pack()

def create_ui():
    # Create the main window
    main = tk.Tk(screenName="Screen Name", baseName="Base Name")

    # Add separate panels
    player_panel = create_player_panel(main)
    player_panel.grid(row=0, column=0)

    library_panel = create_games_panel(main)
    library_panel.grid(row=0, column=1)

    achievement_panel = create_achievement_panel(main)
    achievement_panel.grid(row=0, column=2)

    # Run window logic and listen for events
    main.mainloop()

create_ui()

# TODO TEMP Roadmap
# Get player data by id input box of some kind
# Game list in a Listbox
# Achievements in a Listbox based on that

# # Create the main window
# root = tk.Tk()
# #root.title("Game Stats Tracker")
# root.config(bg="#121212")

# style = ttk.Style(root)
# style.configure("TLabel", background="#121212", foreground='#ffffff')

# # Define the fonts
# font_arial = ("Arial", 12)
# font_times = ("Times New Roman", 12)
# font_roboto = ("Roboto", 12)
# font_segoe = ("Segoe UI", 12)
# font_open_sans = ("Open Sans", 12)
# font_montserrat = ("Montserrat", 12)
# font_lato = ("Lato", 12)
# font_exo = ("Exo", 12)

# # Create a label with the chosen font
# label = ttk.Label(root, text="Game Stats: Arial", font=font_arial, style="TLabel")
# label.pack(padx=10, pady=10)
# label = ttk.Label(root, text="Game Stats: Roboto", font=font_roboto, style="TLabel")
# label.pack(padx=10, pady=10)
# label = ttk.Label(root, text="Game Stats: Segoe UI", font=font_segoe, style="TLabel")
# label.pack(padx=10, pady=10)
# label = ttk.Label(root, text="Game Stats: Times New Roman", font=font_times, style="TLabel")
# label.pack(padx=10, pady=10)
# label = ttk.Label(root, text="Game Stats: Open Sans", font=font_open_sans, style="TLabel")
# label.pack(padx=10, pady=10)
# label = ttk.Label(root, text="Game Stats: Montserrat", font=font_montserrat, style="TLabel")
# label.pack(padx=10, pady=10)
# label = ttk.Label(root, text="Game Stats: Lato", font=font_lato, style="TLabel")
# label.pack(padx=10, pady=10)
# label = ttk.Label(root, text="Game Stats: Exo", font=font_exo, style="TLabel")
# label.pack(padx=10, pady=10)


# # Run the Tkinter event loop
# root.mainloop()