import pyvista as pv
import numpy as np
import svgwrite

def slice_stl(path):
    mesh = pv.read(path)
    z_start = 0
    z_end = 10
    slices = mesh.slice_along_axis(axis="z", n=10, bounds=(0, 0, 0, 0, z_start, z_end))
    return slices

def export_stl(slices, path):
    # Create a plotter object
    plotter = pv.Plotter(off_screen=True)

    for i, slice in enumerate(slices):
        # Create an SVG drawing object
        file_path = f"{path}\slice_{i}.svg"
        dwg = svgwrite.Drawing(file_path)

        # Convert the slice to an SVG path
        path = svgwrite.path.Path(d=slice)

        # Add the path to the SVG drawing
        dwg.add(path)

        # Save the SVG file
        dwg.save()

def polydata_to_pyvista():
    p1 = pv.Plotter(notebook=False)
    p1.add_mesh(poly, label="Test label <")
    p1.add_legend()
    p1.save_graphic('test.svg', raster=False)

path = r"C:\Users\antwi87\Documents\GitHub\obpgenerator-1\src\testfiles\test_fork.stl"
temp = r"C:\Users\antwi87\Downloads\svg_files"

slices = slice_stl(path)
paths = slices[9].points
print(paths)
print(slices[0].lines)
#print(slices[0].lines)
#export_stl(slices, temp)


