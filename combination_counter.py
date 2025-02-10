import random

import pandas as pd
import datetime

results = []

filename = "D:\\Github\\tools\\generated\\cleaned_results.xlsx"
# filename = input("get the filename to be checked:\n")

data: list = []
game = "Superlotto 6/49"


# "Lotto 6/42", "Megalotto 6/45", "Superlotto 6/49", "Grand Lotto 6/55", "Ultra Lotto 6/58"


# get all saturdays

# for each saturday get all game results from previous friday to dates less than 4 days

def get_all_saturdays() -> list:
    date_to = datetime.datetime.today().date()
    date_from = datetime.datetime.strptime('11/12/14', '%m/%d/%y').date()
    difference = (date_to - date_from).days
    print(difference)
    saturdays = [date_from + datetime.timedelta(days=x) for x in range(difference) if
                 (date_from + datetime.timedelta(days=x)).weekday() == 5]
    return saturdays


def count_numbers_from_combinations(exclude_642: bool, max_results: int = 0) -> None:
    df: pd.DataFrame
    try:
        df = pd.read_excel(filename, skiprows=0)

        for k, v in df.iterrows():
            if exclude_642:
                if v["LOTTO GAME"] != game:
                    continue

            results.append(str(v["COMBINATIONS"]))
            if len(results) >= max_results:
                break

    except Exception as e:
        print(e)

    results_dict = {}

    print(f'results count : {len(results)}')
    for combi in results:
        result_list = combi.split("-")
        for number in result_list:
            if int(number) > 49:
                continue

            if number not in results_dict.keys():
                results_dict[number] = 1
            else:
                results_dict[number] = results_dict[number] + 1

    sorted_result_counter = {}

    count_set = set(results_dict.values())

    count_list = list(count_set)
    count_list.reverse()
    print(count_list)

    for count in count_list:
        for k, v in results_dict.items():
            # ignore the number greater than 42
            if int(k) > 49:
                continue
            if v == count:
                sorted_result_counter[k] = count

    print(f"number count : {len(sorted_result_counter.keys())}")

    for k, v in sorted_result_counter.items():
        print(k, v)

    for_random = list(sorted_result_counter.keys())[4:]
    rnd = random.Random()
    for i in range(4):
        num = rnd.randint(0, 30)
        print(num)


count_numbers_from_combinations(max_results=10, exclude_642=False)
