import json
import pandas as pd

try:
    # Load JSON data
    with open(r'D:\Github\tools\target\earthquake.json', 'r') as file:
        print(file)
        data = json.load(file)
except FileNotFoundError:
    print("Error: 'data.json' not found.")
except json.JSONDecodeError:
    print("Error: Invalid JSON format in 'data.json'.")

df = pd.DataFrame([data])

destination = r"D:\Github\tools\generated\earthquake_minimized.json"

filtered_df = df.filter(like="Philippines")

print(len(filtered_df))
print(len(df))
#
# with open(destination, 'w') as file:
#     json.dumps(df.)
#
# try:
#
#     writer_book = pd.ExcelWriter(path=destination)
#     sheet = str("data")
#     df = pd.DataFrame(data)
#     df.to_excel(writer_book, sheet_name=sheet, index=False)
#
#     writer_book.close()
# except Exception as e:
#     print(e)
