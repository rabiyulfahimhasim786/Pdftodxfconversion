import os
import ezdxf

# Set the folder path containing the DXF files
folder_path = 'dxf_files'

# Create a new DXF file to merge all the entities
merged_doc = ezdxf.new('R2010')
merged_msp = merged_doc.modelspace()

# Loop through all DXF files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.dxf'):
        # Create a new DXF document for the current file
        doc = ezdxf.readfile(os.path.join(folder_path, filename))
        msp = doc.modelspace()
        # Loop through each entity in the file and add it to the merged DXF file
        for entity in msp:
            # Create a new Line entity in the merged DXF file
            if entity.dxftype() == 'LINE':
                start = entity.dxf.start
                end = entity.dxf.end
                merged_line = merged_msp.add_line(start, end)
            else:
                # Copy the entity to the merged DXF file
                merged_entity = entity.copy()
                # Add the copied entity to the modelspace of the merged DXF file
                merged_msp.add_entity(merged_entity)

# Save the merged DXF file
merged_doc.saveas(os.path.join(folder_path, 'merged_file.dxf'))