#!/usr/bin/env python3

import os
import sys
import argparse
import pathlib
import random
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
    from PIL import Image
    from inky.auto import auto
except ImportError:
    print("Error: Inky or PIL not found. Ensure they are installed in the 'pimoroni' venv.")
    sys.exit(1)

# --- CONFIGURATION ---
IMAGE_DIR = "/home/display/inky/images"
LAST_IMAGE_FILE = "/home/display/inky/last_image.txt"

try:
    inky = auto(ask_user=True, verbose=True)
except TypeError:
    inky = auto()

parser = argparse.ArgumentParser()
parser.add_argument("--saturation", "-s", type=float, default=0.5, help="Colour palette saturation")
parser.add_argument("--file", "-f", type=pathlib.Path, help="Image file")

args, _ = parser.parse_known_args()
saturation = args.saturation

# --- IMAGE SELECTION WITH DUPLICATION CHECK ---
path_obj = Path(IMAGE_DIR)
png_files = list(path_obj.glob('*.png'))

if not png_files:
    print(f"Error: No .png files found in {IMAGE_DIR}")
    sys.exit(1)

# Read the last image used
last_image = ""
if Path(LAST_IMAGE_FILE).exists():
    last_image = Path(LAST_IMAGE_FILE).read_text().strip()

# Choose a new image
random_filename = random.choice(png_files)

# Avoid repeats if possible
if len(png_files) > 1:
    while str(random_filename) == last_image:
        random_filename = random.choice(png_files)

# Record the choice
Path(LAST_IMAGE_FILE).write_text(str(random_filename))

# --- DISPLAY LOGIC ---
image = Image.open(random_filename)
resized_image = image.resize(inky.resolution)

inky.set_image(resized_image, saturation=saturation)
inky.show()

print(f"Displayed image: {random_filename}")
