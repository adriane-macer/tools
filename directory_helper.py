import os

# Specify the directory name
directory_name = "GFG"


for x in range(100):
    # Create the directory
    try:
        # os.mkdir("generated\\" + str(x+1).zfill(3))
        # print(f"Directory '{x}' created successfully.")
        print("-\t" + "assets/images/avatars/" + str(x+1).zfill(3) + "/")
    except FileExistsError:
        print(f"Directory '{x}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{x}'.")
    except Exception as e:
        print(f"An error occurred: {e}")