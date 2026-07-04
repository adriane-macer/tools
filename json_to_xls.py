import json
import pandas as pd

# Load JSON data
with open(r'D:\Github\tools\target\cat_mafia_boss.json', "r", encoding="utf-8") as file:
    data = json.load(file)

df = pd.DataFrame([data])
df.to_excel(r'D:\Github\tools\target\generated\cat_mafia_boss.xlsx', index=False)

writer_book: pd.ExcelWriter
destination = r"D:\Github\tools\target\generated\cat_mafia_boss.xlsx"
try:

    writer_book = pd.ExcelWriter(path=destination)
    sheet = str("data")
    df = pd.DataFrame(data)
    df.to_excel(writer_book, sheet_name=sheet, index=False)

    writer_book.close()
except Exception as e:
    print(e)
