import math 
import numpy as np
import math
import file_import
import line_melting
import obplib as obp
import manufacturing_settings as settings
import generate_obp

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



class Shape:
    def __init__(self):
        self.paths = [] #array of matplotlib.path
        self.keep_matrix = None #matrix defining which mesh elements that should be kept
        self.coord_matrix = None #matrix defining the coordinates of the mesh elements
        self.obp_points = [] #array with elements that build your obp file, contains arrays with 1, 2, or 4 obp.Points. 1 Point in array = obplib.TimedPoints, 2 points = obplib.Line, 4 points = obp.Curve
        self.nmb_of_scans = 1 #Number of times the shape should be scanned
        self.manufacturing_settings = settings.ManufacturingSetting() #Manufacturing settings
        self.obp_elements = [] #array with elements for exports

    def generate_matrixes(self, spacing, size=150, angle=0): #spacing and size in mm, angle in degree 
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
    def generate_obp_elements(self):
        same_elements = []
        self.obp_elements = []
        for i, element in enumerate(self.obp_points):
            if len(same_elements) == 0 or len(element) == len(same_elements[0]):
                same_elements.append(element)
            if len(element) != len(same_elements[0]) or i == len(self.obp_points)-1:
                if len(same_elements[0]) == 1:
                    self.obp_elements = self.obp_elements + generate_obp.generate_points(same_elements,self.manufacturing_settings)
                elif len(same_elements[0]) == 2:
                    self.obp_elements = self.obp_elements + generate_obp.generate_lines(same_elements,self.manufacturing_settings)
                elif len(same_elements[0]) == 4:
                    self.obp_elements = self.obp_elements + generate_obp.generate_curves(same_elements,self.manufacturing_settings)
                same_elements = [element]
    def export_obp(self, filename):
        self.generate_obp_elements()
        obp.write_obp(self.obp_elements, filename)
    def export_obpj(self,filename):
        self.generate_obp_elements()
        obp.write_obpj(self.obp_elements, filename)
    def line_melt(self,strategy ="snake"):
        if strategy == "snake":
            lines = line_melting.line_snake(self)
            self.obp_points = self.obp_points + lines
        elif strategy == "left_to_right":
            lines = line_melting.line_left_right(self)
            self.obp_points = self.obp_points + lines
        elif strategy == "right_to_left":
            lines = line_melting.line_right_left(self)
            self.obp_points = self.obp_points + lines
    def point_melt(self, strategy="random", settings=[]):
        if strategy == "random":
            None
class Layer:
    def __init__(self):
        self.shapes = [] #array of shape objects
class Part:
    None

new_shape = Shape()
new_shape.generate_matrixes(1,size=20)
file_path = r"C:\Users\antwi87\Documents\GitHub\obpgenerator\src\testfiles\simple_cube_10_10.svg"
#file_path = r"C:\Users\antwi87\Downloads\testtest.svg"
svg_path = file_import.import_svg_layer(file_path)
matplot_path = file_import.svgpath_to_matplotpath(svg_path)
new_shape.paths = matplot_path
new_shape.check_keep_matrix()

new_shape.line_melt(strategy="left_to_right")

#with np.printoptions(threshold=np.inf):
#    print(new_shape.keep_matrix.astype('int'))
#    print(new_shape.coord_matrix)

new_shape.export_obp(r"C:\Users\antwi87\Downloads\testtest.obp")

