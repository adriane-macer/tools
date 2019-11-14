import os

files = [f for f in os.listdir("C:\\Users\\Evangelista\\Music\\Bibles")]

for file in files:
    new_name = file.split("\uf026")[-1]
    src = "C:\\Users\\Evangelista\\Music\\Bibles\\" + file
    dst = "C:\\Users\\Evangelista\\Music\\renamed\\" + new_name
    os.rename(src, dst)
