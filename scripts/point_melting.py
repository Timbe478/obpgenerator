import numpy as np
import obplib

def point_random(shape):
    nmb_of_elements_to_melt = np.sum(shape.keep_matrix.astype('int'))
    order = np.arange(nmb_of_elements_to_melt)
    np.random.shuffle(order)
    positions_to_melt = np.transpose(np.nonzero(shape.keep_matrix))
    points_to_melt = []
    for i in order:
        xPos = positions_to_melt[i][0]
        yPos = positions_to_melt[i][1]
        points_to_melt.append([obplib.Point(shape.coord_matrix[xPos][yPos].real*1000, shape.coord_matrix[xPos][yPos].imag*1000)])
    return points_to_melt