import pandas as pd
import json
import os
import datetime

def start_converting(filename, destination):
    xls = pd.ExcelFile(filename)

    xls.sheet_names


    print(xls.sheet_names)
    for sheet_name in xls.sheet_names:
        excel_df = None
        try:
            excel_df = pd.read_excel(filename, skiprows=0, sheet_name=sheet_name)
        except Exception as e:
            print(e)
            return False

        data = []


        for k, v in excel_df.iterrows():
            data.append(v.to_dict())

        try:
            with open(destination +  "\\" + sheet_name + ".json", 'a+', ) as f:
                json.dump(data, f, indent=4, )
        except Exception as e:
            print(e)
            return False

    return True


def run():
    print("converting from excel to json...")
    destination_directory = ""
    source_directory = ""

    is_valid_destination = False
    is_valid_source = False

    while not is_valid_source:
        source_filename = input("Enter the filename to be converted.")
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

    success = start_converting(filename=source_filename,
                               destination=destination_directory)

    if (success):
        print("done conversion")
    else:
        print("conversion failed.")


if __name__ == '__main__':
    run()
