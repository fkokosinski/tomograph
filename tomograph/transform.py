import numpy as np


def translate(x, y):
    """ Return translation matrix. """
    return np.array([
        [1, 0, x],
        [0, 1, y],
        [0, 0, 1],
    ])


def rotate(a):
    """ Return rotation matrix.  """
    return np.array([
        [np.cos(a), np.sin(a), 0],
        [-np.sin(a), np.cos(a), 0],
        [0, 0, 1]
    ])
