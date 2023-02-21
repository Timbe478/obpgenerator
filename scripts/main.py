import math 
import numpy as np
import math
import file_import
import line_melting

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in degree.
    """
    angle = math.radians(angle)
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

class ManufacturingSetting:
    def __init__(self):
        pass
class Shape:
    def __init__(self):
        self.paths = [] #array of matplotlib.path
        self.keep_matrix = None #matrix defining which mesh elements that should be kept
        self.coord_matrix = None #matrix defining the coordinates of the mesh elements
        self.obp_elements = [] #array with elements that build your obp file, contains arrays with 1, 2, or 4 obp.Points. 1 Point in array = obplib.TimedPoints, 2 points = obplib.Line, 4 points = obp.Curve
        self.nmb_of_scans = 1 #Number of times the shape should be scanned
        #Base settings
        self.spot_size = 1
        self.beam_power = 1500
        self.dwell_time = 70000

    def generate_matrixes(self, spacing, size, angle=0):
        row_height = math.sqrt(3/4)*spacing
        points_x = math.floor(size/spacing)
        points_y = math.floor(size/row_height)
        self.coord_matrix = np.zeros((points_y, points_x),dtype=np.complex_)
        self.keep_matrix = np.zeros((points_y, points_x))
        
        for i in range(points_x):
            for ii in range(points_y):
                if (ii % 2) == 0:
                    x = i*spacing - size/2
                    y = ii*row_height - size/2
                    if angle != 0:
                        x,y = rotate((0,0),(x,y),angle)
                    self.coord_matrix[ii][i] = complex(x,y)
                else:
                    x = i*spacing - size/2 + spacing/2
                    y = ii*row_height - size/2
                    if angle != 0:
                        x,y = rotate((0,0),(x,y),angle)
                    self.coord_matrix[ii][i] = complex(x,y)
    def check_keep_matrix(self):
        if len(self.paths)>0:
            flatten_keep = self.coord_matrix.flatten()
            flatten_2D = np.column_stack((flatten_keep.real,flatten_keep.imag))
            keep_array = file_import.check_points_in_path(self.paths,flatten_2D)
            self.keep_matrix = keep_array.reshape(self.keep_matrix.shape)
    def generate_obp_file(self):
        None
    def line_melt(self,strategy ="snake"):
        if strategy == "snake":
            lines = line_melting.line_snake(self)
            self.obp_elements.append(lines)
        elif strategy == "left_to_right":
            lines = line_melting.line_left_right(self)
            self.obp_elements.append(lines)
        elif strategy == "right_to_left":
            lines = line_melting.line_right_left(self)
            self.obp_elements.append(lines)
class Layer:
    def __init__(self):
        self.shapes = [] #array of shape objects

class Part:
    None

new_shape = Shape()
new_shape.generate_matrixes(1, 6, angle=0)

file_path = r"C:\Users\antwi87\Downloads\testtest.svg"
svg_path = file_import.import_svg_layer(file_path)
matplot_path = file_import.svgpath_to_matplotpath(svg_path)
new_shape.paths = matplot_path
new_shape.check_keep_matrix()
new_shape.line_melt()
print(new_shape.obp_elements)
#print(lines[0][0])
