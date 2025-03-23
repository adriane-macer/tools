import os
import time

from PIL import Image
import json

# target directory
target = "D:\\Github\\tools\\generated\\avatars\\original"
destination = "D:\\Github\\tools\\generated\\avatars\\cropped_avatars"

# get directories
folders = [f for f in os.listdir(target) if os.path.isdir(target + "\\" + f)]

# print(folders)
# iterate the directories

prefixes = ["Character-In Car_", "Character-Driving_", "Character-Parachute_", "Character-Flying_", "Droid-Fly_"]

map_prefixes = {"Character-In Car_": {
    "left": 55,
    "top": 151,
    "right": 519,
    "bottom": 487
}, "Character-Driving_": {
    "left": 90,
    "top": 76,
    "right": 528,
    "bottom": 481
}, "Character-Parachute_": {
    "left": 164,
    "top": 61,
    "right": 408,
    "bottom": 467
}, "Character-Flying_": {
    "left": 171,
    "top": 26,
    "right": 436,
    "bottom": 433
}, "Droid-Fly_": {
    "left": 195,
    "top": 55,
    "right": 377,
    "bottom": 300
}}

for folder in folders:
    folder_target = target + "\\" + folder
    # get the filenames on each directory
    # get only png files
    pngs = [f for f in os.listdir(folder_target) if os.path.isfile(folder_target + "\\" + f) and f.endswith(".png")]

    # get the filecount on each directory
    count = len(pngs)

    # create json for the properties of the file
    # rename each file in the directory

    destination_folder = destination + "\\" + folder
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
            destination_file = destination + "\\" + folder + "\\" + new_filename + ".png"
            left = map_prefixes[found_prefix]["left"]
            right = map_prefixes[found_prefix]["right"]
            top = map_prefixes[found_prefix]["top"]
            bottom = map_prefixes[found_prefix]["bottom"]

            print(f'===>{destination_file}')
            # print(f'=>>>{folder_target}/{png_file}')
            # Opens a image in RGB mode
            im = Image.open(f'{folder_target}\\{png_file}')

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
