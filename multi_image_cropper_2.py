import os
import time

from PIL import Image
import json

# target directory
target = input("input target directory:\n")

target_paths = target.split("\\")
destination_folder = f'./generated/avatars/cropped_avatars/{target_paths[len(target_paths) - 1]}'

prefixes = ["Character-In Car_", "Character-Driving_", "Character-Parachute_", "Character-Flying_", "Droid-Fly_"]

pngs = [f for f in os.listdir(target) if os.path.isfile(target + "\\" + f) and f.endswith(".png")]

# get the filecount on each directory
count = len(pngs)

# create json for the properties of the file
# rename each file in the directory


left = int(input("left: "))
top = int(input("top: "))
width = int(input("width: "))
height = int(input("height: "))
right = left + width
bottom = top + height

if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

for png_file in pngs:
    new_filename = png_file.removesuffix(".png")
    found_prefix = None
    for prefix in prefixes:
        if png_file.__contains__(prefix):
            new_filename = new_filename.removeprefix(prefix)
            found_prefix = prefix
            break

    if len(new_filename) > 3:
        print(new_filename)
    try:
        destination_file = destination_folder + "\\" + new_filename + ".png"

        # print(f'=>>>{folder_target}/{png_file}')
        # Opens a image in RGB mode
        im = Image.open(f'{target}\\{png_file}')

        # Cropped image of above dimension
        # (It will not change original image)
        im1 = im.crop((left, top, right, bottom))

        # Shows the image in image viewer
        im1.save(destination_file)
    finally:
        pass

# Define student_details dictionary
sprite_properties = {
    "count": count,
}

# Convert and write JSON object to file
with open(destination_folder + "\\" + "sprite_properties.json", "w") as outfile:
    json.dump(sprite_properties, outfile)
