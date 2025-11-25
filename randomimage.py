#!/usr/bin/env python3

import argparse
import pathlib
import sys
import glob
import random
from pathlib import Path
from PIL import Image
from inky.auto import auto

try:
    inky = auto(ask_user=True, verbose=True)
except TypeError:
    inky = auto()

parser = argparse.ArgumentParser()
parser.add_argument("--saturation", "-s", type=float, default=0.5, help="Colour palette saturation")
parser.add_argument("--file", "-f", type=pathlib.Path, help="Image file")

args, _ = parser.parse_known_args()

saturation = args.saturation

path_str=r"Your Path Here"
path_obj = Path(path_str)

png_files = list(path_obj.glob('*.png'))

if not png_files:
    print(f"Error: No.png files found in directory: {path_str}")
else:
    random_filename = random.choice(png_files)
    image = Image.open(random_filename)
    resized_image = image.resize(inky.resolution)

    # 1. Apply saturation to the image for the Inky display
    inky.set_image(resized_image, saturation=saturation)

    # 2. Update the display
    inky.show()
    print(f"Displayed image: {random_filename}")
