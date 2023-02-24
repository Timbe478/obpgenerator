import obplib

def generate_obp_points(line_coords):
    line_points = []
    print(line_coords)
    for coord in line_coords:
        start_point = obplib.Point(coord[0].real*1000, coord[0].imag*1000)
        end_point = obplib.Point(coord[1].real*1000, coord[1].imag*1000)
        line_points.append([start_point,end_point])
    return line_points
        

def find_firsts(row, order=1): #order = 1 meanse left to right, -1 means right to left
    first = []
    if order == 1:
        for i in range(len(row)):
            if i == 0:
                if row[i]:
                    first.append(i)
            else:
                if row[i] and row[i-1]==False:
                    first.append(i)
    else:
        for i in range(len(row)-1,-1,-1):
            if i == len(row)-1:
                if row[i]:
                    first.append(i)
            else:
                if row[i] and row[i+1]==False:
                    first.append(i)
    return first
def find_lasts(row,order=1):
    lasts = []
    if order == 1:
        for i in range(len(row)):
            if i == len(row)-1:
                if row[i]:
                    lasts.append(i)
            else:
                if row[i] and row[i+1]==False:
                    lasts.append(i)
    else:
        for i in range(len(row)-1,-1,-1):
            if i == 0:
                if row[i]:
                    lasts.append(i)
            else:
                if row[i] and row[i-1]==False:
                    lasts.append(i)
    return lasts

def line_snake(shape):
    lines = []
    (x,y) = shape.keep_matrix.shape
    for i in range(x):
        if (i % 2) == 0:
            first = find_firsts(shape.keep_matrix[i])
            lasts = find_lasts(shape.keep_matrix[i])
        else:
            first = find_firsts(shape.keep_matrix[i],order=-1)
            lasts = find_lasts(shape.keep_matrix[i],order=-1)
        for ii in range(len(first)):
            lines.append((shape.coord_matrix[i][first[ii]],shape.coord_matrix[i][lasts[ii]]))
    line_points = generate_obp_points(lines)
    return line_points
def line_left_right(shape):
    lines = []
    (x,y) = shape.keep_matrix.shape
    for i in range(x):
        first = find_firsts(shape.keep_matrix[i])
        lasts = find_lasts(shape.keep_matrix[i])
        for ii in range(len(first)):
            lines.append((shape.coord_matrix[i][first[ii]],shape.coord_matrix[i][lasts[ii]]))
    line_points = generate_obp_points(lines)
    return line_points
def line_right_left(shape):
    lines = []
    (x,y) = shape.keep_matrix.shape
    for i in range(x):
        first = find_firsts(shape.keep_matrix[i],order=-1)
        lasts = find_lasts(shape.keep_matrix[i],order=-1)
        for ii in range(len(first)):
            lines.append((shape.coord_matrix[i][first[ii]],shape.coord_matrix[i][lasts[ii]]))
    line_points = generate_obp_points(lines)
    return line_points
        
            