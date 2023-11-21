## DXF Merger

This is for merging multiple dxf files into one dxf file.

### How To Use

- Install Dependencies

  > python -m pip install -r requirements.txt

- Run

  > python main.py

- You can edit data.json file to change input folder+files, output folder+file:


```
{
    "desc": "files for a demo dxf merger based on ezdxf",
    "pathin": "in/",
    "pathout": "out/",
    "targetfile": "merge.dxf",
    "use_filelist": true,
    "filelist": ["page_1.dxf", "page_2.dxf", "page_3.dxf", "page_4.dxf", "page_5.dxf"],
}
```
