import shutil
import os


def copy_and_rename_file(source_path, destination_directory, new_file_name):
    try:
        # Construct the full path for the new file in the destination directory
        destination_path = os.path.join(destination_directory, new_file_name)

        # Copy the file
        shutil.copy(source_path, destination_path)
        print(
            f"File '{os.path.basename(source_path)}' copied to '{destination_directory}' as '{new_file_name}' successfully.")

    except FileNotFoundError:
        print(f"Error: Source file '{source_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def list_directories(path):
    directories = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            directories.append(item)
    return directories


source_directory = r"D:\Github\tools\target\avatars"  # Replace with your actual source file path
destination_folder = r"D:\Github\tools\target\generated\preview_avatars"  # Replace with your actual destination directory path
# renamed_file = "renamed_file.txt"  # Replace with your desired new file name

directories = list_directories(source_directory)

for directory in directories:

    folder = directory.split('\\')[-1]
    if len(folder) == 3:
        renamed_file = f'{folder}.png'
        try:
            target_file = f'{source_directory}\\{folder}\\00.png'

            copy_and_rename_file(target_file, destination_folder, renamed_file)

        except Exception as e:
            print(f"{folder} : {e}")
