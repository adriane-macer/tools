import os
import shutil
import json

# target directory
target = "D:\\Github\\tools\\generated\\avatars\\original"
destination = "D:\\Github\\tools\\generated\\avatars\\renamed"

# get directories
folders = [f for f in os.listdir(target) if os.path.isdir(target + "\\" + f)]

# print(folders)
# iterate the directories

prefixes = ["Character-In Car_", "Character-Driving_", "Character-Parachute_", "Character-Flying_", "Droid-Fly_"]

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
        for prefix in prefixes:
            new_filename = new_filename.removeprefix(prefix)
        if len(new_filename) > 3:
            print(new_filename)
        try:
            shutil.copy(src=folder_target + "\\" + png_file,
                        dst=destination + "\\" + folder + "\\" + new_filename + ".png")
            # os.rename(src=folder_target + "\\" + png_file,
            #           dst=destination + "\\" + folder + "\\" + new_filename + ".png")
        finally:
            pass

    # Define student_details dictionary
    sprite_properties = {
        "count": count,
    }

    # Convert and write JSON object to file
    with open(destination_folder + "\\" + "sprite_properties.json", "w") as outfile:
        json.dump(sprite_properties, outfile)
