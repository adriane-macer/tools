import datetime
import pandas as pd
import json
import os


def start_training(filename, destination):
    date_to = datetime.datetime.strptime('2/11/24', '%d/%m/%y').date()
    date_from = datetime.datetime.strptime('1/1/14', '%d/%m/%y').date()

    list_sheet_data = []
    last_row_position = 0

    saturdays = get_saturdays(date_from=date_from, date_to=date_to)
    saturdays.reverse()
    print(saturdays)
    for saturday in saturdays:
        pos, result = compare_combi_with_previous(row_starting_position=last_row_position,
                                                  winning_date=saturday,
                                                  num_rows=20)
        # print(f'pos, result : {pos} , {result}')
        last_row_position = pos
        list_sheet_data.append(result)
        break

    print(len(list_sheet_data))
    print(list_sheet_data)

    return True


def convert_date_draw(date_draw) -> datetime.date:
    date_draw_split = date_draw.split("-")
    date_draw_day = date_draw_split[1]
    date_draw_month = date_draw_split[2]
    date_draw_year = date_draw_split[0][2:]
    converted = datetime.date

    try:
        converted = datetime.datetime.strptime(f'{date_draw_day}/{date_draw_month}/{date_draw_year}', '%d/%m/%y').date()
    except:
        converted = datetime.datetime.strptime(f'{date_draw_month}/{date_draw_day}/{date_draw_year}', '%d/%m/%y').date()
    finally:
        return converted


def compare_combi_with_previous(row_starting_position: int, winning_date: datetime.date,
                                num_rows: int) -> (
        int, pd.DataFrame):
    # use global or variable
    filename = "D:\\Github\\tools\\cleaned_results_10Nov_2024.xlsx"
    data: pd.DataFrame
    new_starting_position = row_starting_position
    counter = 0
    row_list = []

    df = pd.read_excel(filename, skiprows=row_starting_position, nrows=num_rows)

    winning_combinations = ""

    for k, v in df.iterrows():

        date_draw = pd.Timestamp(f"{str(v['DRAW DATE'])}").date()

        date_draw_converted = convert_date_draw(str(date_draw))

        game = str(v["LOTTO GAME"])

        if date_draw_converted == winning_date and game == "Lotto 6/42":
            winning_combinations = str(v["COMBINATIONS"])

    winning_combinations_split = winning_combinations.split("-")
    print(f'Winning Combinations : {winning_combinations}')

    for k, v in df.iterrows():
        game = str(v["LOTTO GAME"])

        date_draw = pd.Timestamp(f"{str(v['DRAW DATE'])}").date()

        date_draw_converted = convert_date_draw(str(date_draw))

        if date_draw_converted > (winning_date - datetime.timedelta(days=7)):
            counter = counter + 1

        if winning_date == date_draw_converted and game == "Lotto 6/42":
            continue

        combinations = str(v["COMBINATIONS"])
        combinations_split = combinations.split("-")

        row_dictionary: dict = {"Date": date_draw, "LOTTO GAME": game}

        matched_count = 0

        # iterates the wining combination and check the matched position of the current game combinations
        for combi in winning_combinations_split:
            print(f"combi            : {combi}")
            for x in range(len(combinations_split)):
                # print(f'combinations_split[x] : {combinations_split[x]}')
                if combi == combinations_split[x]:
                    row_dictionary[x+1] = str(x+1)
                    print(f'x     : {x}')
                    print(f'x row : {row_dictionary}')
                    matched_count = matched_count + 1
                else:
                    row_dictionary[x+1] = ""

        row_dictionary["Matched Count"] = matched_count

        row_list.append(row_dictionary)

        # print(f'row_dictionary : {row_dictionary}')
        counter = counter + 1

    data = pd.DataFrame(row_list)
    return counter + row_starting_position, data


def get_saturdays(date_from: datetime.date, date_to: datetime.date) -> list:
    print(f'date_to {date_to}')
    print(f'date_from {date_from}')
    difference = (date_to - date_from).days
    print(difference)
    saturdays = [date_from + datetime.timedelta(days=x) for x in range(difference + 1) if
                 (date_from + datetime.timedelta(days=x)).weekday() == 5]
    return saturdays


def run():
    global source_filename
    print("cleaning results")
    destination_directory = ""
    source_directory = ""

    is_valid_destination = False
    is_valid_source = False

    # while not is_valid_source:
    #     source_filename = input("Enter the filename to be cleaned.\n")
    #     if source_filename.endswith('.xls'):
    #         pass
    #     elif source_filename.endswith('.xlsx'):
    #         pass
    #     else:
    #         print("{} is not a valid excel file.".format(source_filename))
    #         print("Please input valid excel file.")
    #         continue
    #
    #     if not os.path.exists(source_filename):
    #         print("Invalid filename.\nPlease try again.")
    #         continue
    #     is_valid_source = True
    # destination_directory = "\\".join(source_filename.split("\\")[:-1])

    success = start_training(filename="D:\\Github\\tools\\cleaned_results_10Nov_2024.xlsx",
                             destination=destination_directory)

    if success:
        print("done Cleaning")
    else:
        print("cleaning failed.")


if __name__ == '__main__':
    run()
