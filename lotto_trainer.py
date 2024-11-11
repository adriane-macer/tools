import datetime
import pandas as pd
import json
import os


def start_training(filename, destination):
    date_from = datetime.datetime.today().date()
    date_to = datetime.datetime.strptime('1/1/14', '%m/%d/%y').date()

    list_sheet_data: []
    last_row_position = 0

    saturdays = get_saturdays(date_from=date_from, date_to=date_to)

    return


def compare_combi_with_previous(row_starting_position: int, winning_date: datetime.date, num_rows: int) -> (
        int, pd.DataFrame):
    # use global or variable
    filename = "D:\\Github\\tools\\cleaned_results_10Nov_2024.xlsx"
    dataframe = None
    new_starting_position = row_starting_position
    with pd.read_excel(filename, skiprows=row_starting_position, nrows=num_rows) as df:
        counter = 0
        for k, v in pd.DataFrame(df).iterrows():
            date_draw = str(v["DRAW_DATE"])
            game = str(v["LOTTO GAME"])
            if str(winning_date) == date_draw and game == "Lotto 6/42":
                new_starting_position = row_starting_position + counter
                continue

            counter = counter + 1


def get_saturdays(date_from: datetime.date, date_to: datetime.date) -> list:
    difference = (date_to - date_from).days
    days = [date_from + datetime.timedelta(days=x) for x in range(difference) if
            (date_from + datetime.timedelta(days=x)).weekday() == 5]
    return days


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

    success = start_training(filename=source_filename,
                             destination=destination_directory)

    if success:
        print("done Cleaning")
    else:
        print("cleaning failed.")


if __name__ == '__main__':
    run()
