from PyPDF2 import PdfReader, PdfWriter

writer = PdfWriter()

for page in reader.pages:
    page.compress_content_streams()
    page.
    writer.add_page(page)

with open("out.pdf", "wb") as f:
    writer.write(f)
