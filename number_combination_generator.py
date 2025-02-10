import random


def generate_n_numbers(combi_length: int, start: int, end: int):
    list_of_numbers = []
    while len(list_of_numbers) < 6:
        n = random.randrange(11, 41)
        if n not in list_of_numbers:
            list_of_numbers.append(n)

    return list_of_numbers


# print(list_of_numbers)

def compare_list(l1: list, l2: list):
    l1.sort()
    l2.sort()
    if l1 == l2:
        return True
    else:
        return False


def has_combination_matched(list_of_combinations: list, number_combination: list):
    has_matched = False
    for combination in list_of_combinations:
        has_matched = compare_list(combination, number_combination)
        if has_matched:
            return True

    return False


def generate_combinations(number_of_combinations: int, combination_length: int, start_range: int, end_range: int):
    list_of_combinations = []
    while len(list_of_combinations) < number_of_combinations:
        combination = generate_n_numbers(combi_length=combination_length, start=start_range, end=end_range)
        has_matched = has_combination_matched(list_of_combinations=list_of_combinations, number_combination=combination)
        if not has_matched:
            list_of_combinations.append(combination)
    return list_of_combinations


generated_combinations = generate_combinations(6, 6, 11, 30)
for comb in generated_combinations: print(comb)
