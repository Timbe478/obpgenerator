# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 14:15:02 2022

@author: willi
"""
import math
import numpy as np
from svgpathtools import svg2paths
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
from obplib.Point import Point as obpPoint
from obplib.Line import Line as obpLine
import obplib as obp
import random
#import xlsxwriter

#########################################################################################################################################################

def load_outline(outline):
    #The function that reads the svg file for a layer. It converts the paths within said svg file to polygons.
    # It returns two lists, polygons and polygon_points. polygons is a list containing shapely polygon objects
    # polygon_points is a 3d array containing the x and y values for all points in all polygons
    
   paths, attributes  = svg2paths(outline)
   polygons = []
   polygon_points = []
   for i in range(len(paths)):
       
       outline_path = paths[i]
       
       number_of_lines = len(outline_path)
       #outline = outline.translated(x+y*1j)
       #depending on where the origin of of the svg file is compared to the origin of the print bed a translate action might be needed.
       #extractiong the points from the path to generate a polygon
       points = []
       
       for j in range(number_of_lines): #extracts the coordinates describing the svg polygon.
           line = outline_path[j]
           point = line[1] 
           coord = [point.real, point.imag]
           points.append(coord)
           

       polygon = Polygon(points)
       polygons.append(polygon)
       polygon_points.append(points)

   return polygons, polygon_points

########################################################################################################################################################

def check_nesting(polygons, polygon_points):
    #Used to identify if the polygonsin the svg file are nested or separate.
    #Returns a square matrix with the of 1:s and 0:s denoting if a polygon is inside of another polygon.
    #Ex: 
    #    [1 1 1 0] The first rows shows the first polygon containing polygon 2 and 3
    #    [0 1 1 0] The second row shows the second polygon containing polygon 3
    #    [0 0 1 0] The third row shows the third polygon only containing itself
    #    [0 0 0 1] The fourth row shows the fourth polygon only containing itself  
    
    le = len(polygons)
    nesting_matrix = np.zeros((le, le))
    for i in range(le):
        polygon = Polygon(polygon_points[i])
        for j in range(le):
            point = Point(polygon_points[j][0])
            
            if i == j :
                nesting_matrix[i][j] = 1
            elif polygon.contains(point):
                
                nesting_matrix[i][j] = 1
            else: 
                nesting_matrix[i][j] = 0

    return nesting_matrix

#########################################################################################################################################################

def generate_points(offset, start, end):
    #Generates equidistant points in rows with a specified offset.
    
    offset = 2*offset/(math.sqrt(5)) 
    points_in_line = int((100/offset)-2) #doubble check the number of points in a line, not entierly sure if the start and end point need to be removed from the total number of not
    coord_array = np.linspace(start, end, points_in_line)
    
    return coord_array

def rotate_points(x_coords, y_coords, angle): 
    #Rotates a coodrinates for a around the origin
    
    im_coords = []
    for i in range(len(x_coords)):
        x_rot = x_coords[i] * math.cos(angle) - y_coords[i] * math.sin(angle)
        y_rot = x_coords[i] * math.sin(angle) + y_coords[i] * math.cos(angle)
        im_coords.append(x_rot + y_rot*1j)    
    
    return im_coords

#########################################################################################################################################################

def draw_pattern(offset, angle):
    #Uses the subfunctions generate_points and rotate points to create a point pattern called dot_matrix spaning the size of the print bed.
    #Returns a 2d array with row length = nr of points in line and colum lenght = number of lines
    
    nr_of_lines = int(100/offset) 
    dot_matrix = []    
    for n in range(nr_of_lines):
        if n % 2 == 0:
            x_start = -50 
            x_end = 50
            y_start = -50+n*offset
            y_end = -50+n*offset
            dot_line_x = generate_points(offset, x_start, x_end) 
            dot_line_y = generate_points(offset, y_start, y_end)
            dot_line_coords = rotate_points(dot_line_x, dot_line_y, angle)
            dot_matrix.append(dot_line_coords)
            
        else:
            x_start = -50+(2*offset/(math.sqrt(5))) 
            x_end = 50+(2*offset/(math.sqrt(5)))
            y_start = -50+n*offset
            y_end = -50+n*offset
            dot_line_x = generate_points(offset, x_start, x_end) 
            dot_line_y = generate_points(offset, y_start, y_end)
            dot_line_coords = rotate_points(dot_line_x, dot_line_y, angle)
            dot_matrix.append(dot_line_coords)
    
    return dot_matrix 

#########################################################################################################################################################

def point_within_polygon(polygon, dot_matrix):
    #Checks which points in the dot_matrix are within a specific polygon
    #Returns a 2d array with the same shape as the dot matrix but with only 1:s and 0:s
    #The 1:s denotes the points in the dot_matrix which are inside the polygon 
    
    rows = len(dot_matrix)
    cols = len(dot_matrix[0])
    shape = (rows, cols)
    keep_matrix = np.zeros(shape)
    for i in range(rows):
        for j in range(cols):
            point_complex = dot_matrix[i][j]
            point = Point(point_complex.real, point_complex.imag)
            if polygon.contains(point) == True:
                keep_matrix[i][j] = 1
            else:
                keep_matrix[i][j] = 0
    
    return  keep_matrix 

#########################################################################################################################################################

def shapes_to_melt(polygons, polygon_points, dot_matrix, nesting_matrix):
    #Identifies which points will be melted. 
    
    nr_of_polygons = len(polygons)
    all_keep_matrices = []
    sum_of_matrices = []
    nesting_level_array = []
    
    for i in range(nr_of_polygons):
        polygon = polygons[i]
        keep_matrix = point_within_polygon(polygon, dot_matrix)
        all_keep_matrices.append(keep_matrix)

    for i in range(nr_of_polygons):
        nesting_level = 0
        for j in range(nr_of_polygons):
            nesting_level = nesting_level+nesting_matrix[j][i] #
        nesting_level_array.append(nesting_level)
    
    
    for i in range(nr_of_polygons):
        if nesting_level_array[i] % 2 == 0:
            all_keep_matrices[i] = -1*all_keep_matrices[i]
        else:
            all_keep_matrices[i] = all_keep_matrices[i]
            
    for i in range(nr_of_polygons):
        if i == 0:
            sum_of_matrices =  all_keep_matrices[i]
        else:
            sum_of_matrices = sum_of_matrices + all_keep_matrices[i]
    
    rows = len(dot_matrix)
    cols = len(dot_matrix[0])
    points_to_melt = []
    for i in range(rows):
        points_in_row = []
        for j in range(cols):
            if sum_of_matrices[i][j] == 1:
                points_in_row.append(dot_matrix[i][j])

        if points_in_row != []: 
            points_to_melt.append(points_in_row)
    
    
    return points_to_melt, sum_of_matrices 

#########################################################################################################################################################

def line_melt_2(dot_matrix, sum_of_matrices, beamparameters):
    #Uses the dot_matrix and the sum_of_matrices to create obp and obpj lines.
    
    loop_length = len(sum_of_matrices)-1
    start_points = []
    end_points = []
    line_melt_pattern = []
    for i in range(loop_length):
        for j in range(loop_length):
            if sum_of_matrices[i][j] == 1 and sum_of_matrices[i][j-1] == 0 and sum_of_matrices[i][j+1] != 0:
                start_point_im = dot_matrix[i][j]
                start_point = obpPoint(start_point_im.real*1000, start_point_im.imag*1000)
                start_points.append(start_point)
            elif sum_of_matrices[i][j] == 1 and sum_of_matrices[i][j+1] == 0 and sum_of_matrices[i][j-1] != 0:
                end_point_im = dot_matrix[i][j]
                end_point = obpPoint(end_point_im.real*1000, end_point_im.imag*1000)
                end_points.append(end_point)

    for i in range(len(start_points)):
        line = obpLine(start_points[i], end_points[i], 10000, beamparameters)
        line_melt_pattern.append(line)
    
    obp.write_obpj(line_melt_pattern, "test.obpj")    
    obp.write_obp(line_melt_pattern, "test.obp")    
        
    
    return

#########################################################################################################################################################

def rand_point_melt(points_to_melt, dwell_time, beamparameters):
    nr_of_lines = len(points_to_melt)
    points = []
    dwell_times = []
    
    for i in range(nr_of_lines):        
        for j in range(len(points_to_melt[i])):
            point = obp.Point(points_to_melt[i][j].real*1000, points_to_melt[i][j].imag*1000)
            points.append(point)
            
            
   
    random.shuffle(points)
        
    for i in range(len(points)): 
        dwell_times.append(dwell_time)
    
    spots = obp.TimedPoints(points, dwell_times, beamparameters)
    pattern = [spots]
    
    obp.write_obpj(pattern, "test.obpj")
    obp.write_obp(pattern, "test.obp")
    
    return

#########################################################################################################################################################

#Paths to svg files for testing
#outline = r'C:\Users\willi\Desktop\SVGslicer\nested_paths.svg'
outline = r'C:\Users\willi\Desktop\SVGslicer\3_paths.svg'
#outline = r'C:\Users\willi\Desktop\SVGslicer\outline.svg'
#paths, attributes  = svg2paths(outline)

#########################################################################################################################################################

# Commands that run the code

polygons, polygon_points = load_outline(outline)

dot_matrix = draw_pattern(1  , 1)

nesting_matrix = check_nesting(polygons, polygon_points)

points_to_melt, sum_of_matrices = shapes_to_melt(polygons, polygon_points, dot_matrix, nesting_matrix)

beamparameters = obp.Beamparameters(100,100)

dwell_time = 70000

point_melt = rand_point_melt(points_to_melt, dwell_time, beamparameters)

#line_melt_pattern = line_melt_2(dot_matrix, sum_of_matrices, beamparameters)


#########################################################################################################################################################

# Commands to run the visualizer 

#              #change working directory and run obp viewer

#              cd C:\Users\willi\Desktop\SVGslicer

#              python obpviewer.py test.obp

#########################################################################################################################################################

#Old line melt function that alternates the direction for each scan line. Does not work for hollow structures or for structures with more than one path

# def line_melt(rows_in_matrix, beamparameters):
#     line_melt_pattern = []
#     for i in range(len(rows_in_matrix)):
#         if i % 2 == 0:
#             start_point_im = rows_in_matrix[i][0]
#             end_point_im = rows_in_matrix[i][-1]
#             start_point = obpPoint(start_point_im.real*1000, start_point_im.imag*1000) #might be a problem with the y coords. have to investigate different angles
#             end_point = obpPoint(end_point_im.real*1000, end_point_im.imag*1000)
#             line = obpLine(start_point, end_point, 10000, beamparameters)
#             #obp.write_obpj([line], "test.obpj")
#             line_melt_pattern.append(line)
            
#         else:
#             start_point_im = rows_in_matrix[i][-1]
#             end_point_im = rows_in_matrix[i][0]
#             start_point = obpPoint(start_point_im.real*1000, start_point_im.imag*1000)
#             end_point = obpPoint(end_point_im.real*1000, end_point_im.imag*1000)
#             line = obpLine(start_point, end_point, 10000, beamparameters)
#             #obp.write_obpj([line], "test.obpj")
#             line_melt_pattern.append(line)
#     obp.write_obpj(line_melt_pattern, "test.obpj")
#     obp.write_obp(line_melt_pattern, "test.obp")
    
#     return


# workbook = xlsxwriter.Workbook('arrays.xlsx')
# worksheet = workbook.add_worksheet()

# #array = point_to_melt_matrix #all points byt zeros othern than the coords for melting
# #array = melting_points #only the meltingpoints

# array = sum_of_matrices

# row = 0

# for col, data in enumerate(array):
#       worksheet.write_column(row, col, data)

# workbook.close()








