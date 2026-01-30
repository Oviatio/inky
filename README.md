🖼️ Inky Impression Display Suite

Transform your Pimoroni Inky Impression (7.3", 5.7", or 4.0") into a rotating digital art gallery. This suite provides two distinct ways to enjoy art: pulling masterpieces directly from the Metropolitan Museum of Art or cycling through your own curated local collection.
🛠️ Hardware & Setup
1. Hardware Requirements

    Display: Pimoroni Inky Impression e-ink display.

    Computer: Raspberry Pi (Zero, 3, 4, or 5).

    Configuration: SPI Interface must be enabled via sudo raspi-config (Interfacing Options > SPI).

2. Python Dependencies

Run the following command to install the required libraries for display control, web requests, and image processing:
Bash

pip3 install inky[rpi] requests Pillow

🚀 The Scripts
🏛️ Met Museum Scraper (met_scrape.py)

Fetches random, public-domain masterpieces from the Metropolitan Museum of Art’s Open Access collection.

    Smart Filtering: Pulls from a user-defined array of department IDs (e.g., European Paintings, Egyptian Art).

    Information Overlay: Automatically adds a high-contrast "plaque" at the bottom-left containing the Title and Artist.

    No Disk Trace: Converts images to PNG in-memory; any temporary files are deleted immediately after the display updates to preserve SD card health.

Execution:
Bash

python3 met_scrape.py

📁 Local Random Gallery (random_image.py)

Cycles through your personal collection of images stored on the Raspberry Pi.

    Custom Library: Ideal for family photos, digital art, or custom-designed PNGs.

    Saturation Control: Includes CLI arguments to tweak color intensity for the e-ink medium.

    Setup: Place your .png files in the images directory:
    Bash

    mkdir -p /home/display/inky/images

Execution:
Bash

# Display with default saturation (0.5)
python3 random_image.py

# Display with maximum color intensity
python3 random_image.py --saturation 1.0

⚙️ Technical Overview
Feature	Met Scraper (met_scrape.py)	Local Gallery (random_image.py)
Data Source	Metropolitan Museum API	/home/display/inky/images
Scaling	ImageOps.fit (Center crop & fill)	image.resize (Stretch to fit)
Resolution	Optimized for 800x480	Auto-detected via inky.resolution
Disk Impact	Clean (Deletes after use)	Persistent (Reads existing files)
Overlay	Artwork Metadata Plaque	None
📅 Automation

Automate your gallery to update every morning (e.g., 8:00 AM) using a cron job.

    Enter the crontab editor: crontab -e

    Add your preferred script path:

Bash

# Example: Daily 8AM Museum Update
0 8 * * * /usr/bin/python3 /home/display/inky/scripts/met_scrape.py

📝 Important Notes

    Refresh Time: E-ink updates are not instant. Expect a 15–40 second refresh cycle as the 7-color palette settles.

    Fonts: The met_scrape.py script looks for fonts in /usr/share/fonts/truetype/dejavu/. Ensure these are installed for the information plaque to render correctly.

    Aspect Ratio: For the random_image.py script, use images matching your screen's aspect ratio to avoid stretching.
