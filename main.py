 
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import os
import datetime
import time

# Determine the base directory of the script to construct absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, 'images')

# Basic setup
root = tk.Tk()
root.title("Pragaras")
root.geometry("800x600")  # Window size
root.config(bg='black')

# Ask for player information
player_name = simpledialog.askstring("Name", "Enter your name:")
player_birth_year = simpledialog.askstring("Year of Birth", "Enter your year of birth:")

# Initialize game variables
current_scene = "connect"
player_alive = True
start_time = time.time()

scenes = {
    "connect": {
        "description": "As you connect your consciousness to the cyber world, a surge of digital energy engulfs you.",
        "image": "infuse.png",
        "options": ["Embrace the connection", "Resist the influx"],
        "next": ["mainframe", "resist"]
    },
    "mainframe": {
        "description": "You're inside the mainframe. Data streams flow around you. Somewhere in here is the demon army's nexus.",
        "image": "infuse.png",
        "options": ["Search for the nexus", "Look for allies"],
        "next": ["nexus", "ally"]
    },
    "resist": {
        "description": "Resisting the connection strains your mind. The demon-infested cyberspace fights back, trying to assimilate you.",
        "image": "not_available.png",
        "options": ["Keep resisting", "Give in"],
        "next": ["gameover", "mainframe"]
    },
    "ally": {
        "description": "A humanoid figure with cybernetic goat features approaches. He's a demon, but his eyes show intelligence and kindness.",
        "image": "npc1.png",
        "options": ["Talk to him", "Ignore him and proceed"],
        "next": ["talk_ally", "nexus"]
    },
    "gameover": {
        "description": "Your mind cannot withstand the cyber onslaught. As your consciousness fades, so does your life in the real world.",
        "image": "game_over.png",
        "options": ["Restart", "Quit"],
        "next": ["connect", "exit"]
    },
    # Additional scenes with "now_available.png" as placeholders
    "hellscape_entry": {
        "description": "The city looms before you, a grotesque blend of decayed skyscrapers and pulsating cybernetics.",
        "image": "now_available.png",
        "options": ["Explore the streets", "Search for survivors"],
        "next": ["streets_exploration", "survivor_search"]
    },
    "streets_exploration": {
        "description": "As you navigate the streets, the air crackles with digital corruption. Something glints among the rubble.",
        "image": "now_available.png",
        "options": ["Investigate the object", "Keep moving"],
        "next": ["journal_discovery", "keep_moving"]
    },
    "journal_discovery": {
        "description": "You find a battered journal, its pages flickering with holographic text. It speaks of the cyber-demons' rise.",
        "image": "now_available.png",
        "options": ["Read more", "Pocket the journal and move on"],
        "next": ["deep_lore", "keep_moving"]
    },
    "deep_lore": {
        "description": "The journal reveals a twisted history of demon and machine, united by hatred for humanity's unconstrained spirit.",
        "image": "now_available.png",
        "options": ["Reflect on this", "Move on"],
        "next": ["reflect_lore", "keep_moving"]
    },
    "reflect_lore": {
        "description": "The revelations weigh heavily on you. The demons' hatred is not baseless, but born of fear and misunderstanding.",
        "image": "now_available.png",
        "options": ["Ponder the implications", "Shake it off and proceed"],
        "next": ["ponder_implications", "hellscape_deeper"]
    },
    "hellscape_deeper": {
        "description": "You delve deeper into the city, where the air hums with power. An ancient facility stands, forgotten.",
        "image": "now_available.png",
        "options": ["Enter the facility", "Circle around cautiously"],
        "next": ["facility_entry", "cautious_approach"]
    },
    "facility_entry": {
        "description": "Inside, darkness greets you. The air is thick with static. Ahead, the silhouette of something immense.",
        "image": "now_available.png",
        "options": ["Approach the figure", "Search for a light source"],
        "next": ["approach_figure", "find_light"]
    },
    "approach_figure": {
        "description": "The figure is a dormant cyber-demon, its form both majestic and terrifying. A console blinks nearby.",
        "image": "now_available.png",
        "options": ["Attempt to activate the demon", "Back away"],
        "next": ["activate_demon", "back_away"]
    },
    "activate_demon": {
        "description": "With a deep hum, the cyber-demon stirs. Its eyes flicker to life, a glow of recognition in their depths.",
        "image": "now_available.png",
        "options": ["Confront the nexus with it", "Attempt to communicate"],
        "next": ["final_confrontation", "communicate_demon"]
    },
    "final_confrontation": {
        "description": "Together, you face the demon army's nexus. The ancient cyber-demon roars, a sound of defiance and liberation.",
        "image": "now_available.png",
        "options": ["Fight alongside the demon", "Let the demon lead"],
        "next": ["fight_together", "demon_leads"]
    },
    "exit": {
        "description": "Thank you for playing. The digital hellscape awaits your return.",
        "image": "now_available.png",
        "options": [],
        "next": []
    }
}
# Function to update the timer
def update_timer():
    elapsed_time = time.time() - start_time
    formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    timer_label.config(text=formatted_time)
    root.after(1000, update_timer)

# Function to update the canvas with an image
def update_canvas_image(image_filename):
    global canvas
    canvas.delete("all")  # Clear the previous image
    image_path = os.path.join(IMAGES_DIR, image_filename)
    try:
        img = Image.open(image_path)

        # Resize the image while maintaining aspect ratio
        base_width = canvas.winfo_width()  # Get the width of the canvas
        w_percent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((base_width, h_size), Image.Resampling.LANCZOS)  # Updated resizing method

        imgTk = ImageTk.PhotoImage(img)
        canvas.image = imgTk  # Keep a reference
        # Update canvas size if needed or you can skip resizing the canvas if you prefer a fixed size
        # canvas.config(width=base_width, height=h_size)
        canvas.create_image(0, 0, anchor='nw', image=imgTk)  # Use anchor='nw' to align the image top-left
    except IOError as e:
        print(e)
        print(f"Error loading the image - {image_path}")


# Function to update the description text
def update_description(description_text):
    description_label.config(text=description_text)

# Function to update the options (buttons) based on the current scene
def update_options(options_list, next_list):
    for widget in button_frame.winfo_children():
        widget.destroy()
    for option, next_scene in zip(options_list, next_list):
        button = tk.Button(button_frame, text=option, command=lambda ns=next_scene: change_scene(ns))
        button.pack()

# Function to show the end credits and total play time
def show_end_credits():
    current_year = datetime.datetime.now().year
    age = current_year - int(player_birth_year)
    age_description = "the wise" if age >= 50 else "the young"
    messagebox.showinfo("End Credits", f"Thank you for playing, {player_name} ({age_description}).\nYour journey has ended, but the digital hellscape awaits your return.")
    root.destroy()

# Function to handle scene changes
def change_scene(scene):
    global current_scene, player_alive
    if scene == "gameover":
        player_alive = False
    current_scene = scene
    scene_data = scenes[scene]
    update_canvas_image(scene_data["image"])
    update_description(scene_data["description"])
    update_options(scene_data["options"], scene_data["next"])
    if not player_alive:
        show_end_credits()

# GUI Layout
canvas = tk.Canvas(root, width=450, height=450, bg='black')
canvas.pack()

description_label = tk.Label(root, fg="white", bg="black", text="")
description_label.pack()

button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X, pady=10)

timer_label = tk.Label(root, text="00:00:00", fg="white", bg="black")
timer_label.pack()

update_timer()  # Start updating the timer

# Make sure the 'scenes' dictionary is correctly populated before calling change_scene
change_scene(current_scene)

root.mainloop()

# todo how much time played
# todo player is referenced by name
# todo based on player age, dialogue will midlly change. if in 20s, ref how young player is. if 50 ref they are a granpda
# todo add gore
# todo add free sounds
# todo add journal player reads, has a few pages to flesh out world building
# todo flesh out plot more
# todo maybe add dice ingame like in dnd, for two enemy fights that will occur
# todo buy health in one part of the game
# todo add hp
# todo chiptune music?
# todo add the npc art
