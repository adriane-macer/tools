from spire.pdf import *
from spire.pdf.common import *

# Create a PdfCompressor object and specify the path of the PDF file to be compressed
input_pdf = "D:\\Github\\tools\\target\\JoshuaOliverEvangelista-RunningBill.pdf"
compressor = PdfCompressor(input_pdf)

# Configure the compression options to optimize images in the PDF
compression_options = compressor.OptimizationOptions
compression_options.SetImageQuality(ImageQuality.Medium)
compression_options.SetResizeImages(True)
compression_options.SetIsCompressImage(True)

# Compress the PDF file and save the result to a new file
output_pdf = "OptimizingImages.pdf"
compressor.CompressToFile(output_pdf)