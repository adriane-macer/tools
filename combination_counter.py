import pandas as pd
import datetime

results = []

filename = "D:\\Github\\tools\\cleaned_results_10Nov_2024.xlsx"
# filename = input("get the filename to be checked:\n")

data: list = []


# get all saturdays

# for each saturday get all game results from previous friday to dates less than 4 days


def get_all_saturdays() -> list:
    date_to = datetime.datetime.today().date()
    date_from = datetime.datetime.strptime('1/1/14', '%m/%d/%y').date()
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
                if v["LOTTO GAME"] != "Lotto 6/42":
                    continue

            results.append(str(v["COMBINATIONS"]))
            if len(results) >= max_results and not max_results != 0:
                break

    except Exception as e:
        print(e)

    results_dict = {}

    for combi in results:
        result_list = combi.split("-")
        for number in result_list:
            if int(number) > 42:
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
    print("37-06-07-18-09-27")

    for count in count_list:
        for k, v in results_dict.items():
            # ignore the number greater than 42
            if int(k) > 42:
                continue
            if v == count:
                sorted_result_counter[k] = count

    print(sorted_result_counter.keys())

    for k, v in sorted_result_counter.items():
        print(k, v)
