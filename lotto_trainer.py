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

    filename = "D:\\Github\\tools\\cleaned_results_10Nov_2024.xlsx"

    dataframe = pd.read_excel(filename, skiprows=0)
    print(f'dataframe length : {len(dataframe)}')

    saturdays_and_pos = list(get_saturdays_with_first_row_number(dataframe=dataframe, days=saturdays))

    for saturday in saturdays_and_pos:
        result = compare_combi_with_previous(dataframe=dataframe, row_starting_position=saturday[1],
                                             winning_date=saturday[0],
                                             num_rows=20)
        list_sheet_data.append(result)

    print(f'list_sheet_data :  : {len(list_sheet_data)}')
    print(f'list_sheet_data : {list_sheet_data}')

    return True


def convert_date_draw(date_draw) -> datetime.date:
    date_draw_split = date_draw.split("-")

    if len(date_draw_split) <= 2:
        print(f'date_draw : {date_draw}; length : {len(date_draw_split)}')
        return  datetime.datetime.strptime('1/1/01', '%d/%m/%y').date()

    date_draw_day = date_draw_split[1]
    date_draw_month = date_draw_split[2][0:2]
    date_draw_year = date_draw_split[0][2:]
    converted = datetime.date

    try:
        converted = datetime.datetime.strptime(f'{date_draw_day}/{date_draw_month}/{date_draw_year}', '%d/%m/%y').date()
    except:
        converted = datetime.datetime.strptime(f'{date_draw_month}/{date_draw_day}/{date_draw_year}', '%d/%m/%y').date()
    finally:
        return converted


def get_next_starting_position(winning_date: datetime.date, df: pd.DataFrame, current_starting: int) -> int:
    filename = "D:\\Github\\tools\\cleaned_results_10Nov_2024.xlsx"
    data: pd.DataFrame

    dataframe = pd.read_excel(filename, skiprows=current_starting, nrows=100)
    counter = 0
    for k, v in dataframe.iterrows():
        date_draw = None
        try:
            date_draw = str(v['DRAW DATE'])
        except Exception as e:
            # print(e)
            continue

        date_draw_converted = convert_date_draw(str(date_draw))

        game = str(v["LOTTO GAME"])
        if date_draw_converted == (winning_date - datetime.timedelta(days=7)) and game == "Lotto 6/42":
            break

        counter = counter + 1

    return counter + current_starting - 1


def get_saturdays_with_first_row_number(dataframe: pd.DataFrame, days: list):
    position = 0
    max_length = len(dataframe)
    for day in days:
        print(f'day : {day}')
        saturday: datetime.date = day
        previous_saturday = saturday - datetime.timedelta(days=7)
        print(f'previous_date : {previous_saturday}')
        has_position: bool = False
        print(f'max_length : {max_length}')
        for x in range(position, max_length - position):
            position = position + 1
            dframe = dataframe.iloc[x]
            print(f'x      : {x}')
            print(f'dframe : {dframe}')
            try:
                draw_date = str(dframe['DRAW DATE'])
                date_draw_converted = convert_date_draw(str(draw_date))

                game = str(dframe["LOTTO GAME"])
                if date_draw_converted == saturday and game == "Lotto 6/42" and not has_position:
                    has_position = True
                    yield date_draw_converted, position

                if date_draw_converted <= previous_saturday:
                    position = position - 1
                    has_position = False
                    break

            except Exception as e:
                print(f'get_saturdays_with_first_row_number : {e}')
                position = position - 1
                has_position = False


def compare_combi_with_previous(dataframe: pd.DataFrame, row_starting_position: int, winning_date: datetime.date,
                                num_rows: int) -> pd.DataFrame:
    row_list = []

    winning_combinations = ""

    print(f'row_starting_position : {row_starting_position}')

    # new_starting_position = get_next_starting_position(winning_date, df, current_starting=row_starting_position)

    for x in range(len(dataframe)):
        df = dataframe.iloc[x]
        date_draw = None
        try:
            date_draw = str(df['DRAW DATE'])
        except Exception as e:
            # print(e)
            continue

        date_draw_converted = convert_date_draw(str(date_draw))

        game = str(df["LOTTO GAME"])

        if date_draw_converted == winning_date and game == "Lotto 6/42":
            winning_combinations = str(df["COMBINATIONS"])

    winning_combinations_split = winning_combinations.split("-")
    print(f'Winning Combinations : {winning_combinations}')

    for i in range(len(dataframe)):
        df = dataframe.iloc[i]
        try:
            game = str(df["LOTTO GAME"])
            date_draw = str(df['DRAW DATE'])

            date_draw_converted: datetime.date = convert_date_draw(str(date_draw))

            if winning_date == date_draw_converted and game == "Lotto 6/42":
                continue

            combinations = str(df["COMBINATIONS"])
            combinations_split = combinations.split("-")

            matched_count = 0

            row_dictionary = {"Date": date_draw, "LOTTO GAME": game, "1": "", "2": "", "3": "", "4": "", "5": "",
                              "6": "", }

            # iterates the wining combination and check the matched position of the current game combinations
            for combi in winning_combinations_split:
                for x in range(len(combinations_split)):
                    # print(f'combinations_split[x] : {combinations_split[x]}')
                    if combi == combinations_split[x]:
                        row_dictionary[str(x + 1)] = str(x + 1)
                        matched_count = matched_count + 1

            row_dictionary["Matched Count"] = matched_count

            row_list.append(row_dictionary)

            # print(f'row_dictionary : {row_dictionary}')
        except Exception as e:
            # print(f' exception : {e}')
            continue

    data = pd.DataFrame(row_list)
    return data


def get_saturdays(date_from: datetime.date, date_to: datetime.date) -> list:
    print(f'date_to {date_to}')
    print(f'date_from {date_from}')
    difference = (date_to - date_from).days
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
