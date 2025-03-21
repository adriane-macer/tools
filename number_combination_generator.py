import random
import time
import pandas as pd


def generate_n_numbers(combi_length: int, start: int, end: int):
    list_of_numbers = []
    delays = {1: 0.000002, 2: 0.00000985005, 3: 0.00004, 4: 0.0000006, 5: 0.000890006, 6: 0.0033806, 7: 0.007340006,
              8: 0.001111006}
    while len(list_of_numbers) < combi_length:
        n = random.randrange(start, end)
        if n not in list_of_numbers:
            list_of_numbers.append(n)
            dly = random.randrange(1, 9)
            time.sleep(delays[dly])

    return list_of_numbers


# print(list_of_numbers)

def compare_list(l1: list, l2: list):
    l1.sort()
    l2.sort()
    # print("="*10)
    # print(l1)
    # print("="*10)
    if len(l1) == len(l2):
        if l1 == l2:
            return True
    else:
        for i in range(len(l2) - 5):
            part_of_list = l2[i: i + 6]
            # print(len(part_of_list))
            # print(l2)
            # print(part_of_list)
            # print("*"*20)
            if l1 == part_of_list:
                return True

    return False


def has_combination_matched(list_of_combinations: list, number_combination: list):
    for combination in list_of_combinations:
        combi = number_combination
        has_matched = compare_list(combination, combi)

        if has_matched:
            print("Matched")
            return True

    return False


def get_previous_results():
    filename = r"D:\Github\tools\642_results.xlsx"
    results = []
    try:
        df = pd.read_excel(filename, sheet_name="Sheet3")

        for v in df.values:
            value = str(v[0]).split("-")
            list_value = []
            for i in value:
                list_value.append(int(i))
            results.append(list_value)
    except Exception as e:
        print(e)

    print(f"count : {len(results)}")

    try:
        df = pd.read_excel(filename, sheet_name="Sheet2")

        for v in df.values:
            value = str(v[0]).split("-")
            list_value = []
            for i in value:
                list_value.append(int(i))
            results.append(list_value)
    except Exception as e:
        print(e)
    finally:
        print(f"count : {len(results)}")
        return results


def generate_combinations(number_of_combinations: int, combination_length: int, start_range: int, end_range: int):
    list_of_combinations = []
    previous_results = get_previous_results()
    while len(list_of_combinations) < number_of_combinations:
        combination = generate_n_numbers(combi_length=combination_length, start=start_range, end=end_range)
        has_matched = has_combination_matched(list_of_combinations=list_of_combinations,
                                              number_combination=combination)
        if has_matched:
            continue

        has_matched = has_combination_matched(list_of_combinations=previous_results, number_combination=combination)
        if has_matched:
            continue

        list_of_combinations.append(combination)

    return list_of_combinations


def write_to_file(combinations: list):
    try:
        filename = r"D:\Github\tools\generated\combinations.xlsx"

        df = pd.DataFrame(combinations)
        df.to_excel(filename, index=False)
        return True

    except Exception as e:
        print(e)
        return False


print("Generation of combinations started....")
generated_combinations = generate_combinations(1000, 6, 11, 41)
print("writing to file")
write_to_file(combinations=generated_combinations)
# for comb in generated_combinations: print(comb)


# get_previous_results()
print("Done")
