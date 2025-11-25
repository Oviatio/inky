# 🖼️ Inky Impression Image Display Script

This script is designed to display a **randomly selected PNG image** from a specified directory onto a **Pimoroni Inky Impression e-ink display**. It automatically detects the connected Inky display and resizes the image to fit its resolution.

-----

## 🛠️ Requirements and Setup

### 1\. Hardware

  * A **Pimoroni Inky Impression** display (e.g., Inky Impression 7.3", 5.7", or 4.0").
  * A compatible single-board computer, such as a Raspberry Pi.

### 2\. Python Dependencies

You need the `inky` library (for display control) and `Pillow` (for image manipulation).

```bash
pip3 install inky[rpi] Pillow
```

*(The `[rpi]` extra installs dependencies specifically for Raspberry Pi use.)*

### 3\. Image Directory

The script is configured to look for images in a specific path.

  * **Create the image folder:**
    ```bash
    mkdir -p /home/display/inky/images
    ```
  * **Add your images:** Place your desired **.png** files into this directory: `/home/display/inky/images`.

-----

## 🚀 How to Run the Script

### 1\. Basic Execution

The script will automatically choose a random `.png` file from the images directory, resize it, and display it on the Inky Impression screen.

```bash
python3 randomimage.py
```

### 2\. Using Arguments

The script supports optional arguments to control the color display and to specify a single file instead of choosing randomly.

#### A. Adjusting Color Saturation (`--saturation`, `-s`)

You can control the intensity of the colors displayed on the e-ink screen. The default is `0.5`.

| Value Range | Effect |
| :--- | :--- |
| **0.0** | Grayscale/B\&W |
| **0.5** (Default) | Standard color mapping |
| **1.0** | Maximum saturation |

**Example:** Running the script with maximum saturation:

```bash
python3 randomimage.py --saturation 1.0
```
## ⚙️ Code Overview

| Section | Functionality |
| :--- | :--- |
| `inky = auto(...)` | **Auto-detects** the specific Inky Impression display model connected and sets up the communication. |
| `path_obj.glob('*.png')` | Finds all files ending in `.png` in the `/home/display/inky/images` folder. |
| `random.choice(png_files)` | Selects a **single, random** image file from the list. |
| `image.resize(inky.resolution)` | **Resizes** the selected image to match the precise resolution of the detected Inky screen (e.g., $800 \times 480$). |
| `inky.set_image(..., saturation=...)` | Applies the image data and the specified color saturation to the display's internal buffer. |
| `inky.show()` | **Updates the e-ink screen** with the contents of the buffer, making the image visible. |

-----
