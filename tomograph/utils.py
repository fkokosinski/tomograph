import numpy as np


def calc_radius(width, height):
    """ Calculate circumscribed circle radius. """
    return np.sqrt(width**2 + height**2)/2


def array_round(array):
    """ Round numpy array and convert it to dtype=int """
    return np.rint(array).astype(int)


def circle_points(angle, num, radius):
    """ Put equidistant points on a circle. """
    sample = np.array([0, -radius])
    span = np.deg2rad(angle)/2
    points = []

    # use sample detector to put points on a circle by rotating it
    for alpha in np.linspace(-span, span, num=num):
        rot_mat = np.array([
            [np.cos(alpha), np.sin(alpha)],
            [-np.sin(alpha), np.cos(alpha)]
        ])
        points.append(sample.dot(rot_mat))

    points = np.array(points)
    return array_round(points)
