#!/usr/bin/env python3

import os
import sys
import argparse
import pathlib
import random
import requests
from io import BytesIO
from pathlib import Path

# --- VIRTUAL ENVIRONMENT ENFORCEMENT ---
# This mirrors the 'source' command by forcing the script to use the venv interpreter
VENV_PYTHON = "/home/display/.virtualenvs/pimoroni/bin/python3"

if sys.executable != VENV_PYTHON:
    if os.path.exists(VENV_PYTHON):
        os.execl(VENV_PYTHON, VENV_PYTHON, *sys.argv)
    else:
        print(f"Error: Virtual environment not found at {VENV_PYTHON}")
        sys.exit(1)

# --- IMPORTS (Loaded after venv check to ensure libraries are found) ---
try:
    from PIL import Image, ImageOps, ImageDraw, ImageFont
    from inky.auto import auto
except ImportError:
    print("Error: Inky or PIL not found. Ensure they are installed in the 'pimoroni' venv.")
    sys.exit(1)

# --- Configuration ---
# Departments: 1(American Decorative Arts), 3(Ancient Near Eastern Art) 4(Arms/Armor), 5(Arts of Africa, Oceania, and the Americas), 6(Asian), 7(Cloisters), 8(Costume Institute), 9(Drawings and Prints), 10(Egyptian), 11(European), 12(European Sculpture and Decorative Arts)
# 13(Greek/Roman), 14(Islamic Art), 15(Robert Lehman), 16(The Libraries), 17(Medieval Art), 18(Musical Instruments), 19(Photographs), 21(Modern)
DEPARTMENTS = [4, 6, 10, 11, 13, 17]
MET_SEARCH_URL = "https://collectionapi.metmuseum.org/public/collection/v1/search"
MET_OBJECT_URL = "https://collectionapi.metmuseum.org/public/collection/v1/objects/"

def get_random_artwork():
    """Selects a random department and finds a public domain artwork."""
    dept_id = random.choice(DEPARTMENTS)
    
    params = {
        "departmentId": dept_id,
        "hasImages": "true",
        "isPublicDomain": "true",
        "q": "*"  # Search for everything within that department
    }
    
    print(f"Searching department ID: {dept_id}...")
    search_resp = requests.get(MET_SEARCH_URL, params=params).json()
    
    if not search_resp.get("objectIDs"):
        return None
    
    obj_id = random.choice(search_resp["objectIDs"])
    obj_data = requests.get(f"{MET_OBJECT_URL}{obj_id}").json()
    
    return {
        "url": obj_data.get("primaryImage"),
        "title": obj_data.get("title", "Unknown Title"),
        "artist": obj_data.get("artistDisplayName", "Unknown Artist")
    }
"""
def add_overlay(img, title, artist):
    Adds a text overlay plaque to the bottom left of the image.
    draw = ImageDraw.Draw(img)
    
    # Try to load a font, fall back to default if not found
    try:
        # Standard path on Raspberry Pi OS
        font_main = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
        font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except:
        font_main = font_sub = ImageFont.load_default()

    # Prepare text
    text_lines = [title[:50], artist[:50]] # Truncate if very long
    
    # Calculate box size (simple padding)
    box_padding = 10
    box_width = 350
    box_height = 60
    
    # Draw a dark semi-transparent-looking rectangle (solid for E-ink)
    # Positioning at bottom-left
    rect_coords = [0, 480 - box_height, box_width, 480]
    draw.rectangle(rect_coords, fill="black")
    
    # Write text
    draw.text((box_padding, 480 - box_height + 5), text_lines[0], fill="white", font=font_main)
    draw.text((box_padding, 480 - box_height + 30), text_lines[1], fill="white", font=font_sub)
    
    return img
"""
def main():
    try:
        display = auto()
    except RuntimeError:
        print("Display not found.")
        return

    art_data = get_random_artwork()
    if not art_data or not art_data['url']:
        return

    # 1. Download image into RAM
    img_resp = requests.get(art_data['url'])
    img = Image.open(BytesIO(img_resp.content))
    
    # 2. Process image
    img = ImageOps.fit(img, (800, 480), centering=(0.5, 0.5))
    #img = add_overlay(img, art_data['title'], art_data['artist'])

    # 3. Convert to PNG format in RAM (to satisfy the requirement)
    # This creates a "virtual file" in your memory
    ram_file = BytesIO()
    img.save(ram_file, format="PNG")
    ram_file.seek(0) # Go back to the start of the virtual file

    # 4. Push to display
    print(f"Updating Inky with: {art_data['title']}")
    display.set_image(img, saturation=0.5)
    display.show()
    
    print("Done! Nothing was saved to disk, so nothing to delete.")

if __name__ == "__main__":

    main()
