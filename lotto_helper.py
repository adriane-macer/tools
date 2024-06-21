import csv
from collections import Counter

past_winners = []

with open('past_winning_numbers.csv', 'r') as file:
    reader = csv.reader(file)
    for r in reader:
        if len(r) >= 1:
            past_winners.append(int(r[0]))

occurrences = Counter(past_winners)

most_common = occurrences.most_common(50)

print("Predicted winning numbers", most_common)
