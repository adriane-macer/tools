from PyPDF2 import PdfReader, PdfWriter

reader = PdfReader("MaryAnnEvangelista-CovidIllnessReport.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.compress_content_streams()
    page.
    writer.add_page(page)

with open("out.pdf", "wb") as f:
    writer.write(f)
