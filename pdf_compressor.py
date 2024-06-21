from PyPDF2 import PdfReader, PdfWriter

reader = PdfReader("fileToCompress.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.compress_content_streams()
    writer.add_page(page)

with open("out.pdf", "wb") as f:
    writer.write(f)
