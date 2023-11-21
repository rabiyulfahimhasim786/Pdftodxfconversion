import ezdxf

import json
from os import listdir
from os.path import isfile, join

# opening JSON file
jsondata = json.load(open("data.json"))

if jsondata["use_filelist"]:
    # it use the hardcode file list from data.json
    files = jsondata["filelist"]
else:
    # alternative way of get filelist only using pathin (no filename hardcoding), only dxf files
    files = [
        f
        for f in listdir(jsondata["pathin"])
        if isfile(join(jsondata["pathin"], f))
        if f.lower().endswith(".dxf")
    ]

# empty target dxf
target_dxf = ezdxf.new("R2000")

# Define the offset for each input DXF file
offset_x = 0.0
offset_y = 0.0
max_height = 0

# merger with filelist
for filename in files:
    # path prepare
    print("input  ->", filename)
    pathfilename = jsondata["pathin"] + filename
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

# save merged dfx target
try:
    print("target ->", jsondata["targetfile"])
    target_dxf.saveas(jsondata["pathout"] + jsondata["targetfile"])
except Exception as e:
    print("Error -> ", e.__class__)
