import numpy as np

def point_random(shape):
    nmb_of_elements_to_melt = np.sum(shape.keep_matrix.astype('int'))
    