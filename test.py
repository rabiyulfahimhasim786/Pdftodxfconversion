import ezdxf
from PIL import Image
import numpy as np
import os

# Directory containing the JPG files
jpg_folder = 'output_jpg'

# Iterate through the JPG files in the folder
for filename in os.listdir(jpg_folder):
    if filename.endswith('.jpg'):
        # Load the image using Pillow
        image = Image.open(os.path.join(jpg_folder, filename))

        # Convert the image to grayscale
        image_gray = image.convert('L')

        # Convert the grayscale image to a NumPy array
        image_array = np.array(image_gray)

        # Create a new DXF document
        doc = ezdxf.new(dxfversion='R2010')

        # Create a new modelspace
        msp = doc.modelspace()

        # Define a scaling factor to adjust the image size in the DXF
        scaling_factor = 0.1  # Adjust as needed

        # Iterate over the image pixels and add lines to the DXF for black pixels
        height, width = image_array.shape
        for y in range(height):
            for x in range(width):
                pixel_value = image_array[y, x]
                if pixel_value < 128:  # Assuming black pixels have a low pixel value
                    x1 = x * scaling_factor
                    y1 = (height - y) * scaling_factor  # Flip y-coordinate
                    x2 = (x + 1) * scaling_factor
                    y2 = (height - y - 1) * scaling_factor  # Flip y-coordinate
                    msp.add_line(start=(x1, y1), end=(x2, y2))

        # Save the DXF file with a corresponding name
        dxf_filename = os.path.splitext(filename)[0] + '.dxf'
        doc.saveas(os.path.join(jpg_folder, dxf_filename))

print("DXF files created for each JPG image in the folder:", jpg_folder)

