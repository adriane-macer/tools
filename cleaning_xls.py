import pandas as pd
import json
import os


def start_cleaning(filename, destination):
    try:
        df = pd.read_excel(filename, skiprows=0)

        print(f'Original number of rows: {df.count()["company_stock"]}')

        # print(f"df: {df}")
        # delete duplicates
        df = df.drop_duplicates()
        # remove row with '%' on company_stock column
        df = df[df["company_stock"].str.contains("%") == False]
        # remove row with '#' on company_stock column
        df = df[df["company_stock"].str.contains("#") == False]
        # remove row with '/' on company_stock column
        df = df[df["company_stock"].str.contains("/") == False]
        # remove row with 'Call ' on company_stock column
        df = df[df["company_stock"].str.contains("Call ") == False]
        # remove row with ': ' on company_stock column
        df = df[df["company_stock"].str.contains(":") == False]
        #
        data : list.__dict__ = []
        for k, v in df.iterrows():
            text = str(v["company_stock"])

            if len(text.split(" ")) > 6:
                if len(str(text).split(" ")) > 7:
                    # print(f'len(str(v["company_stock"]).split(" ")) : {len(str(v["company_stock"]).split(" "))}')
                    # print(f"++++ exclude : {v['company_stock']}  +++++")
                    continue

            try:
                if not text.isascii():
                    print(text)
                    continue
            except UnicodeError:
                continue

            # print(f'v {v}')
            # print(f'v.to_dict() : {v.to_dict()}')
            data.append(v.to_dict())
            # print(f"data : {data}")
            # break

        # return False
        # print(f"data : {data}")
        print(f"data count : {len(data)}")

        # convert data to df
        cleaned_df = pd.DataFrame.from_dict(data)

        print(f'Cleaned to {cleaned_df.count()["company_stock"]} number of rows')
        cleaned_df.to_excel(f'{destination}/cleaned.xlsx', index=False)
        print(f'destination: {destination}')
        # return df_to_json(cleaned_df, destination)
        return dict_to_json(data, destination)
    except Exception as e:
        print(e)
        return False


def dict_to_json(data, destination):
    try:
        with open(destination + "\\" + "cleaned.json", 'w', ) as f:
            json.dump(data, f, indent=4, )
    except Exception as e:
        print(e)
        return False

    return True


def df_to_json(df, destination):
    data = []

    for k, v in df.iterrows():
        data.append(v.to_dict())

    try:
        with open(destination + "\\" + "cleaned.json", 'w', ) as f:
            json.dump(data, f, indent=4, )
    except Exception as e:
        print(e)
        return False

    return True


def run():
    global source_filename
    print("converting from excel to json...")
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
