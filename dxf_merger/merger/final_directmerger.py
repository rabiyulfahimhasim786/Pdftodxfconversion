from os import listdir
from os.path import isfile, join
import ezdxf

# Input Directory
path_in = "in/"
# Input files
# files_in = ["page_1.dxf", "page_2.dxf", "page_3.dxf", "page_4.dxf"]
files_in = ["page_1.dxf", "page_2.dxf", "page_3.dxf"]
# Output Directory
path_out = "out/"
# Output file
file_out = "merge.dxf"
"""
use_file_list 
( If it's set to True, will use the hardcoded dxf files from 'files_in'
If it's set to False, will use all dxf files in 'path_in' directory
Default is True )
"""
use_file_list = True

if not use_file_list:
    files_in = [
        f
        for f in listdir(path_in)
        if isfile(join(path_in, f))
        if f.lower().endswith(".dxf")
    ]

# empty target dxf
target_dxf = ezdxf.new("R2000")

# Define the offset for each input DXF file
offset_x = 0.0
offset_y = 0.0
max_height = 0
dxffile_messages = ''
# filenamess= []
# for filename in files_in:
#     try:
#         print("input  ->", filename)
#         pathfilename = path_in + filename
#         filenoext = filename.split(".")[0]
#         append_dxf = ezdxf.readfile(pathfilename)
#         dxffile_messages = f"Dxf file successfully merged"
#         filenamess.append(filename)
#     except IOError:
#         dxffile_messages = f"Not a DXF file or a generic I/O error."
#     except ezdxf.DXFStructureError:
#         dxffile_messages = f"Invalid or corrupted DXF file."
#     except Exception as e:
#         dxffile_messages = f"Error -> {e.__class__}"
# print(filenamess)
# merger with filelist
for filename in files_in:
# for filename in filenamess:
    try:
        # path prepare
        print("input  ->", filename)
        pathfilename = path_in + filename
        filenoext = filename.split(".")[0]
        append_dxf = ezdxf.readfile(pathfilename)
     
        # Get the modelspace of the input file
        modelspace = append_dxf.modelspace()

        # Calculate the height of the DXF file
        for entity in modelspace:
            if entity.dxftype() == 'LINE':
                start = entity.dxf.start
                if max_height < start[1]:
                    max_height = start[1]
                end = entity.dxf.end
                if max_height < end[1]:
                    max_height = end[1]
            elif entity.dxftype() == 'SPLINE':
                control_points = entity._control_points
                for item in control_points:
                    if max_height < item[1]:
                        max_height = item[1]
            elif entity.dxftype() == 'CIRCLE' or entity.dxftype() == 'ARC' or entity.dxftype() == 'ELLIPSE':
                center = entity.dxf.center
                if max_height < center[1] * 2:
                    max_height = center[1] * 2
            elif entity.dxftype() == 'POLYLINE':
                points = entity.points()
                for item in points:
                    if max_height < item[1]:
                        max_height = item[1]
            else:
                if max_height < 30:
                    max_height = 30

        # Create new block definition for the input file
        block_def = target_dxf.blocks.new(name=filename)

        # Iterate over each entity in the modelspace
        for entity in modelspace:
            # Copy the entity to the new block definition
            block_def.add_entity(entity.copy())

        # Create an insert entity for the block definition
        target_dxf.modelspace().add_blockref(
            name=filename,
            insert=(offset_x, offset_y),
            dxfattribs={
                "xscale": 1.0,
                "yscale": 1.0,
                "rotation": 0.0,
            }
        )

        # Increment the offset for the next file
        offset_y -= (max_height * 1.2)
        dxffile_messages = f"Dxf file successfully merged"
    except IOError:
        dxffile_messages = f"Not a DXF file or a generic I/O error."
    except ezdxf.DXFStructureError:
        dxffile_messages = f"Invalid or corrupted DXF file."
    except Exception as e:
        dxffile_messages = f"Error -> {e.__class__}"
    print(dxffile_messages)
# save merged dfx target
try:
    print("target ->", file_out)
    target_dxf.saveas(path_out + file_out)
except Exception as e:
    print("Error -> ", e.__class__)
