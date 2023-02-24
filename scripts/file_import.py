from svgpathtools import svg2paths
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.path as mpltPath

def import_svg_part(file_path): #imports an svg file (path) containing MULTIPLE layers
    tree = ET.parse(file_path)
    root = tree.getroot()
    groups = root.findall(r"{http://www.w3.org/2000/svg}g")
    paths, attributes  = svg2paths(file_path)
    svg_layers = []
    i = 0
    for group in groups:
        local_layer = []
        for shapes in group:
            local_layer.append(paths[i])
            i = i + 1
        svg_layers.insert(0,local_layer)
    return svg_layers
def import_svg_layer(file_path):#imports an svg file (path) containing ONE layer
    svg_layer, attributes  = svg2paths(file_path)
    return svg_layer
def svgpath_to_matplotpath(svg_paths):
    matplotpaths = []
    for path in svg_paths:
        new_path_points = []
        new_path_points.append([path[0].start.real,path[0].start.imag])
        for line in path:
            new_path_points.append([line.end.real,line.end.imag])
        new_path = mpltPath.Path(new_path_points)
        matplotpaths.append(new_path)
    return matplotpaths
def check_points_in_path(matplotpaths, points):
    #points N*2 numpy array
    inside_all = np.full((len(points),), False)
    for path in matplotpaths:
        inside = path.contains_points(points)
        inside_all = np.logical_or(inside_all, inside)
    return inside_all


#file_path = r"C:\Users\antwi87\Documents\GitHub\obpgenerator-1\src\testfiles\test_fork.svg"
#file_path = r"C:\Users\antwi87\Downloads\testtest.svg"
#svg_path = import_svg_layer(file_path)
#matplot_path = svgpath_to_matplotpath(svg_path)
#points = np.random.rand(2,2)
#print(points)
#inside = check_points_in_path(matplot_path,points)
#print(inside)





