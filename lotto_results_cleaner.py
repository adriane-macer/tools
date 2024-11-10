from datetime import datetime
import pandas as pd
import json
import os


def start_cleaning(filename, destination):
    games = ("Lotto 6/42", "Megalotto 6/45", "Superlotto 6/49", "Grand Lotto 6/55", "Ultra Lotto 6/58")
    try:
        df = pd.read_excel(filename, skiprows=0)

        data: list = []
        for k, v in df.iterrows():
            game = str(v["LOTTO GAME"])
            if game not in games:
                continue

            date_str = str(v["DRAW DATE"])

            if type(v["DRAW DATE"]) is str:
                date_in_list = date_str.split("/")
                if len(date_in_list[2]) != 2:
                    new_v = v
                    new_v["DRAW DATE"] = datetime.strptime(
                        f'{date_in_list[0]}/{date_in_list[1]}/{date_in_list[2][2:4]}', '%m/%d/%y').date()
                    data.append(new_v)
                else:
                    new_v = v
                    new_v["DRAW DATE"] = datetime.strptime(date_str, '%m/%d/%y').date()
                    data.append(new_v)

            else:
                new_v = v
                new_v["DRAW DATE"] = (v["DRAW DATE"]).date()
                data.append(new_v)

        print(len(data))
        df = pd.DataFrame(data)
        df.to_excel("cleaned_results_11Nov_2024.xlsx")
        return True

    except Exception as e:
        print(e)
        return False


def run():
    global source_filename
    print("cleaning results")
    destination_directory = ""
    source_directory = ""

    is_valid_destination = False
    is_valid_source = False

    while not is_valid_source:
        source_filename = input("Enter the filename to be cleaned.\n")
        if source_filename.endswith('.xls'):
            pass
        elif source_filename.endswith('.xlsx'):
            pass
        else:
            print("{} is not a valid excel file.".format(source_filename))
            print("Please input valid excel file.")
            continue

        if not os.path.exists(source_filename):
            print("Invalid filename.\nPlease try again.")
            continue
        is_valid_source = True
    destination_directory = "\\".join(source_filename.split("\\")[:-1])

    success = start_cleaning(filename=source_filename,
                             destination=destination_directory)

    if success:
        print("done Cleaning")
    else:
        print("cleaning failed.")


if __name__ == '__main__':
    run()
