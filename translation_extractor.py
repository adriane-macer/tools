import pandas as pd
import json
import os
import datetime


def start_converting(filename, destination):
    xls = pd.ExcelFile(filename)

    # translation type
    sheet_names = xls.sheet_names

    print(sheet_names)
    languages_dict = dict()
    for sheet_name in sheet_names:
        excel_df = None
        try:
            excel_df = pd.read_excel(filename,
                                     header=0,
                                     index_col=0,
                                     sheet_name=sheet_name)
            print(excel_df.head(5))
            print(excel_df.columns)

            languages = excel_df.columns

            for language in languages:
                print(language)
                current_dict = dict()
                if languages_dict.get(language) is None:
                    print("{} is None".format(language))
                    languages_dict.update({language: dict()})
                else:
                    current_dict = languages_dict[language]

                language_series = excel_df[language]
                # print(language_series)

                language_df = language_series.to_frame()

                type_dict = dict()
                type_items_dict = dict()

                for k, v in language_df.iterrows():
                    # print("k {}".format(k))
                    # print("v {}".format(v[language]))
                    if v[language] is None:
                        continue

                    type_items_dict.update({k: v[language]})

                type_dict.update({sheet_name: type_items_dict})

                current_dict.update(type_dict)
                print(current_dict)
                languages_dict.update({language: current_dict})

        except Exception as e:
            print(e)
            return False

    for item in languages_dict.items():
        try:
            with open(destination + "\\" + item[0] + ".json", 'a+', ) as f:
                json.dump(item[1], f, indent=4, )
        except Exception as e:
            print(e)
            return False
        finally:
            xls.close()
        print("item : {}".format(item))

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
