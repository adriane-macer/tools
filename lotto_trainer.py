import datetime
import pandas as pd
import openpyxl

game_to_train = "Superlotto 6/49"
game_max_num = "49"
day_to_train = "sunday"
day_map = {"monday": 0,
           "tuesday": 1,
           "wednesday": 2,
           "thursday": 3,
           "friday": 4,
           "saturday": 5,
           "sunday": 6,
           }

today = datetime.datetime.today().strftime("%m-%d-%y")

# "Lotto 6/42", "Megalotto 6/45", "Superlotto 6/49", "Grand Lotto 6/55", "Ultra Lotto 6/58"


def start_training(filename, destination):
    date_to = datetime.datetime.strptime('14/11/24', '%d/%m/%y').date()
    date_from = datetime.datetime.strptime('1/1/20', '%d/%m/%y').date()

    list_sheet_data = []
    last_row_position = 0

    days = get_days_to_train(date_from=date_from, date_to=date_to)
    days.reverse()

    print(f"ljskdlfkjlskdj : {len(days)}")

    filename = f"D:\\Github\\tools\\generated\\cleaned_results.xlsx"

    dataframe = pd.read_excel(filename, skiprows=0)

    days_and_pos = list(get_days_with_first_row_number(dataframe=dataframe, days=days))

    for day_pos in days_and_pos:
        print('-----------------')
        print(f'day_pos[0] : {day_pos[0]}')
        print(f'day_pos[1] : {day_pos[1]}')
        result = compare_combi_with_previous(dataframe=dataframe, row_starting_position=day_pos[1],
                                             winning_date=day_pos[0], num_rows=20, winning_combinations=day_pos[2])
        # print(f'result  : {len(result)}')
        list_sheet_data.append((day_pos[0], result))

    print(f'list_sheet_data :  {len(list_sheet_data)}')
    # print(f'list_sheet_data : {list_sheet_data}')

    writer_book: pd.ExcelWriter
    destination = f"D:\\Github\\tools\\generated\\trained_output_{game_max_num}_{today}.xlsx"
    try:
        # empty_df = pd.DataFrame({})
        # empty_df.to_excel(destination)

        # Generating workbook and writer engine
        # excel_workbook = openpyxl.load_workbook(destination,data_only=False,read_only=False)
        writer_book = pd.ExcelWriter(path=destination)
        # writer_book = excel_workbook

        for sheet_data in list_sheet_data:
            print(f'sheet : {sheet_data[0]}')
            print(f'sheet_data[1]  : {sheet_data[1]}')
            sheet = str(sheet_data[0])
            df = pd.DataFrame(sheet_data[1])
            print(f'-------- {df}')
            df.to_excel(writer_book, sheet_name=sheet, index=False)

        writer_book.close()
    except Exception as e:
        print(e)

    return True


def convert_date_draw(date_draw) -> datetime.date:
    date_draw_split = date_draw.split("-")

    if len(date_draw_split) <= 2:
        print(f'date_draw : {date_draw}; length : {len(date_draw_split)}')
        return datetime.datetime.strptime('1/1/01', '%d/%m/%y').date()

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


def get_days_with_first_row_number(dataframe: pd.DataFrame, days: list):
    position = 0
    max_length = len(dataframe)
    for day in days:
        # print(f'day : {day}')
        saturday: datetime.date = day
        previous_saturday = saturday - datetime.timedelta(days=7)
        has_position: bool = False
        for x in range(position, max_length - position):
            position = position + 1
            dframe = dataframe.iloc[x]
            try:
                draw_date = str(dframe['DRAW DATE'])
                date_draw_converted = convert_date_draw(str(draw_date))

                game = str(dframe["LOTTO GAME"])
                if date_draw_converted == saturday and game == game_to_train and not has_position:
                    winning_combinations = str(dframe["COMBINATIONS"])
                    has_position = True
                    yield date_draw_converted, position, winning_combinations

                if date_draw_converted <= previous_saturday:
                    position = position - 1
                    break

            except Exception as e:
                print(f'get_saturdays_with_first_row_number : {e}')
                # has_position = False


def compare_combi_with_previous(dataframe: pd.DataFrame, row_starting_position: int, winning_date: datetime.date,
                                num_rows: int, winning_combinations: str) -> pd.DataFrame:
    row_list = []

    # print(f'row_starting_position : {row_starting_position}')

    # new_starting_position = get_next_starting_position(winning_date, df, current_starting=row_starting_position)

    max_length = row_starting_position + num_rows if len(dataframe) >= row_starting_position + num_rows else len(
        dataframe) - row_starting_position

    winning_combinations_split = winning_combinations.split("-")
    print(f'Winning Combinations : {winning_combinations}')

    for i in range(row_starting_position - 1, max_length):
        df = dataframe.iloc[i]
        try:
            game = str(df["LOTTO GAME"])
            date_draw = str(df['DRAW DATE'])

            date_draw_converted: datetime.date = convert_date_draw(str(date_draw))

            if winning_date == date_draw_converted and game == game_to_train:
                continue

            combinations = str(df["COMBINATIONS"])
            combinations_split = combinations.split("-")

            matched_count = 0

            row_dictionary = {"Date": date_draw, "LOTTO GAME": game, "1": "", "2": "", "3": "", "4": "", "5": "",
                              "6": "", }

            # iterates the wining combination and check the matched position of the current game combinations
            for n in range(len(winning_combinations_split)):
                for x in range(len(combinations_split)):
                    # print(f'combinations_split[x] : {combinations_split[x]}')
                    if winning_combinations_split[n] == combinations_split[x]:
                        row_dictionary[str(x + 1)] = str(n + 1)
                        matched_count = matched_count + 1

            row_dictionary["Matched Count"] = matched_count

            row_list.append(row_dictionary)

            # print(f'row_dictionary : {row_dictionary}')
        except Exception as e:
            # print(f' exception : {e}')
            continue

    data = pd.DataFrame(row_list)
    return data


def get_days_to_train(date_from: datetime.date, date_to: datetime.date) -> list:
    print(f'date_to {date_to}')
    print(f'date_from {date_from}')
    difference = (date_to - date_from).days
    saturdays = [date_from + datetime.timedelta(days=x) for x in range(difference + 1) if
                 (date_from + datetime.timedelta(days=x)).weekday() == day_map[day_to_train]]
    return saturdays


def run():
    global source_filename
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

    success = start_training(filename="D:\\Github\\tools\\generated\\cleaned_results.xlsx",
                             destination=destination_directory)

    if success:
        print("done Training")
    else:
        print("Training failed.")


if __name__ == '__main__':
    run()
