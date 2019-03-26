import numpy as np


def projective(coords):
    """ Convert 2D cartesian coordinates to homogeneus/projective. """
    num = np.shape(coords)[0]
    w = np.array([[1], ]*num)

    return np.append(coords, w, axis=1)


def cartesian(coords):
    """ Convert 2D homogeneus/projective coordinates to cartesian. """
    return coords[:, :2]


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
        [np.cos(a), -np.sin(a), 0],
        [np.sin(a), np.cos(a), 0],
        [0, 0, 1]
    ])


def transform_list(coords, matrix):
    """ Apply transformation to a list of coordinates. """
    return matrix.dot(coords.T).T


def transform_apply(coords, transforms):
    """ Apply list of transformations to a list of coordinates. """
    out = coords
    transforms_r = transforms[::-1]

    for transform in transforms_r:
        out = transform_list(out, transform)

    return out
