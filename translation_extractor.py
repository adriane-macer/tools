import pandas as pd
import json
import os
import datetime

def start_converting(filename, destination):
    xls = pd.ExcelFile(filename)

    # translation type
    sheet_names = xls.sheet_names

    print(sheet_names)
    for sheet_name in sheet_names:
        excel_df = None
        try:
            excel_df = pd.read_excel(filename,
                                     header=0,
                                     index_col=0,
                                     # skiprows=0,
                                     sheet_name=sheet_name)
            print(excel_df.head(5))
            print(excel_df.columns)
            print(excel_df['tl'])
            tl = excel_df['tl']
            tl_value = pd.DataFrame(data=tl.values, columns=['tl'])
            tl_index = pd.DataFrame(data=tl.index, columns=['tl'])
            tl_df = pd.merge(tl_index, tl_value, left_index=True, right_index=True)
            print(type(tl_df))

            data = []
            for k, v in tl_df.iterrows():
                print("k {}".format(k))
                print("v {}".format(v))
                print("dict {}".format(v.to_dict()))
                data.append(v.to_dict())

            # TODO remove
            return True

        except Exception as e:
            print(e)
            return False

        data = []

        for k, v in excel_df.iterrows():
            data.append(v.to_dict())

        try:
            with open(destination + "\\" + sheet_name + ".json", 'a+', ) as f:
                json.dump(data, f, indent=4, )
        except Exception as e:
            print(e)
            return False
        finally:
            xls.close()

    return True


def run():
    global source_filename
    print("converting from excel to json...")
    destination_directory = ""
    source_directory = ""

    is_valid_destination = False
    is_valid_source = False

    while not is_valid_source:
        source_filename = input("Enter the filename to be converted.\n")
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

    print("source filename {}".format(source_filename))
    print("destination directory {}".format(destination_directory))
    success = start_converting(filename=source_filename,
                               destination=destination_directory)

    if success:
        print("done conversion")
    else:
        print("conversion failed.")


if __name__ == '__main__':
    run()
