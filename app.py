# import fitz  # PyMuPDF
# from PIL import Image
# import os
# import subprocess

# from pdf2image import convert_from_path
# pages = convert_from_path('3321718_PrintDXf.pdf', 500)

# for count, page in enumerate(pages):
#     page.save(f'out{count}.jpg', 'JPEG')
# # Path to the input PDF file
# pdf_file = '3321718_PrintDXf.pdf'

# # Create a directory to save the images
# output_folder = 'output_images'
# os.makedirs(output_folder, exist_ok=True)

# # Open the PDF file
# pdf_document = fitz.open(pdf_file)

# # Iterate through each page in the PDF
# for page_number in range(len(pdf_document)):
#     # Get the page
#     page = pdf_document[page_number]

#     # Convert the page to a PIL Image
#     image = page.get_pixmap()

#     # Create a filename for the image (e.g., page1.png)
#     image_filename = f'{output_folder}/page{page_number + 1}.jpg'
    

#     # Save the image
#     image.save(image_filename, 'JPEG')

# # Close the PDF file
# pdf_document.close()

# print("PDF pages converted to images and saved in the folder:", output_folder)

from pdf2image import convert_from_path
import os

# Create a folder to save the JPEG files
output_folder = 'output_jpg'
os.makedirs(output_folder, exist_ok=True)

pages = convert_from_path('3321718_PrintDXf.pdf', 500)

for count, page in enumerate(pages):
    # Define the file path for each JPEG file within the output folder
    file_path = os.path.join(output_folder, f'out{count}.jpg')
    page.save(file_path, 'JPEG')
