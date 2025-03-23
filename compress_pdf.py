from pypdf import PdfWriter

target_file = input("Input target file: ")
target_paths = target_file.split("\\")
destination_file = f'./generated/converted_pdf/{target_paths[len(target_paths) - 1]}'

writer = PdfWriter(clone_from=target_file)

for page in writer.pages:
    page.compress_content_streams(level=9)  # This is CPU intensive!

with open(destination_file, "wb") as f:
    writer.write(f)