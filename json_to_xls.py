import json
import pandas as pd

# Load JSON data
with open(r'D:\Github\tools\target\avatars.json') as file:

    data = json.load(file)

df = pd.DataFrame([data])
df.to_excel(r'D:\Github\tools\target\generated\avatars.xlsx', index=False)

writer_book: pd.ExcelWriter
destination = r"D:\Github\tools\target\generated\avatars.xlsx"
try:

    writer_book = pd.ExcelWriter(path=destination)
    sheet = str("data")
    df = pd.DataFrame(data)
    df.to_excel(writer_book, sheet_name=sheet, index=False)

    writer_book.close()
except Exception as e:
    print(e)
