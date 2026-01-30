🖼️ Inky Impression Display Suite

A collection of Python scripts designed for the Pimoroni Inky Impression (7.3", 5.7", or 4.0") to transform your e-ink display into a rotating art gallery. This suite includes tools to pull masterpieces from the Metropolitan Museum of Art or cycle through your personal local collection.
🛠️ Hardware & Setup
1. Hardware Requirements

    Raspberry Pi (Zero, 3, 4, or 5)

    Pimoroni Inky Impression display

    SPI Interface enabled (via sudo raspi-config)

2. Python Dependencies

Install the necessary libraries for display control, web requests, and image processing:
Bash

pip3 install inky[rpi] requests Pillow

🚀 The Scripts
1. Met Museum Scraper (met_scrape.py)

This script fetches random, public-domain masterpieces from the Metropolitan Museum of Art’s Open Access collection.

    Curated Departments: Pulls from user defined array of departments

    Information Overlay: Optionally adds a high-contrast black "plaque" at the bottom with the Title and Artist.

    Auto-Cleanup: Converts the image to PNG for processing but automatically deletes the file after it is displayed to save disk space.

Run it:
Bash

python3 met_scrape.py

2. Local Random Gallery (random_image.py)

Displays a randomly selected .png image from a specified directory on your Raspberry Pi.

    Custom Library: Perfect for personal photos or specific art collections.

    Saturation Control: Supports command-line arguments to tweak color intensity.

    Setup: Create the image folder and add your files:
    Bash

    mkdir -p /home/display/inky/images

Run it:
Bash

# Basic run
python3 random_image.py

# Run with maximum color saturation
python3 random_image.py --saturation 1.0

⚙️ Technical Overview
Feature	Met Scraper (met_scrape.py)	Local Gallery (random_image.py)
Source	Metropolitan Museum API	/home/display/inky/images
Image Handling	ImageOps.fit (Center crop/fill)	image.resize (Stretch to fit)
Resolution	Hardcoded 800×480	Auto-detected via inky.resolution
Storage	Temporary (Deleted after use)	Permanent (Reads from disk)
Overlay	Artist & Title plaque	None
📅 Automation (Cron Job)

To make your display update automatically (e.g., every morning at 8:00 AM), use a cron job.

    Open crontab: crontab -e

    Add a line for your preferred script:
    Bash

    # Update with a new Met painting every morning
    0 8 * * * /usr/bin/python3 /home/display/inky/scripts/met_scrape.py

📝 Notes

    Resolution: The Met script is optimized for the 7.3" display (800×480 pixels).

    E-Ink Refresh: Updates take approximately 15–40 seconds depending on your model. This is normal for multi-color e-ink.

    Formatting: If using the Met script, ensure you have fonts installed at /usr/share/fonts/truetype/dejavu/.
