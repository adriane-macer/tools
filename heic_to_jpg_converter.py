from PIL import Image
from pathlib import Path
from pillow_heif import register_heif_opener

# Register HEIC opener
register_heif_opener()

# Path to the directory containing HEIC images
images_path = Path('D:\\Github\\tools\\target\\heif')

destination_path = "D:\\Github\\tools\\generated\\converted_from_heif"

# Iterate through all HEIC files in the directory
for image_file in images_path.rglob("*.[hH][eE][iI][Cc]"):
    print(f"Converting: {image_file.name}")

    # Open the HEIC file
    image = Image.open(image_file)

    # Convert and save as JPG
    new_name = f".\\generated\\converted_from_heif\\{image_file.stem}.jpg"
    image.convert('RGB').save(new_name)
    print(f"Saved as: {new_name}")