import PyPDF2

# Open the PDF file in read-binary mode
with open('example.pdf', 'rb') as pdf_file:
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Loop through each page in the PDF file
    for page_num in range(len(pdf_reader.pages)):
        # Create a new PDF writer object
        pdf_writer = PyPDF2.PdfWriter()

        # Add the current page to the PDF writer object
        pdf_writer.add_page(pdf_reader.pages[page_num])

        # Save the current page as a new PDF file
        with open(f'page_{page_num+1}.pdf', 'wb') as output_file:
            pdf_writer.write(output_file)