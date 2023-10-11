import ezdxf
import os

# Directory containing the individual DXF files
dxf_folder = 'output_jpg'

# Create a new DXF document for merging
merged_doc = ezdxf.new(dxfversion='R2010')

# Iterate through the DXF files in the folder
for filename in os.listdir(dxf_folder):
    if filename.endswith('.dxf'):
        dxf_path = os.path.join(dxf_folder, filename)

        # Open each individual DXF file
        source_doc = ezdxf.readfile(dxf_path)

        # Merge the entities from the individual DXF file into the merged document
        for entity in source_doc.modelspace().query('*'):
            merged_doc.modelspace().add_entity(entity.clone())

# Save the merged DXF document
merged_doc.saveas('merged_output.dxf')

print("All DXF files merged into 'merged_output.dxf'")
