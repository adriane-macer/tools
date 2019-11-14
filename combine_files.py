import os

root_folder = input("Input target directory")
folders = [f for f in os.listdir(root_folder) if os.path.isdir(root_folder + "\\" + f)]
print(folders)
for folder in folders:
    dst = root_folder + "\\" + folder
    combined_file_name = folder + "_combined_files"
    files = [f for f in os.listdir(dst) if os.path.isfile(dst + "\\" + f)]

    combined_text = ""
    for file in files:
        try:
            with open(
                    dst + "\\" + file,
                    "r", encoding="utf-8") as f:
                combined_text = combined_text + f.read()
        except UnicodeEncodeError as e:
            raise e

    try:
        os.makedirs(dst + "\\" + combined_file_name)
        print("...{} directory created".format(combined_file_name))
    except Exception as e:
        print(e)
        print("Error in creation of whole book directory")
        if not str(e).find("file already exist"):
            print("file already exist")

    try:
        with open(
                dst + "\\" + combined_file_name + "\\" + combined_file_name + ".txt",
                "w", encoding="utf-8") as f:
            f.write(combined_text)
    except UnicodeEncodeError as e:
        raise e
