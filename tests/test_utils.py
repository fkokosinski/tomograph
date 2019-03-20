import numpy as np
from pytest import approx
from tomograph.utils import calc_radius, array_round, circle_points


def test_calc_radius():
    shape = (250, 300)
    radius = calc_radius(*shape)

    assert radius == approx(195.2562)


def test_array_round():
    arr = np.array([0.2, 0.4, 0.6, 0.8])
    expected = np.array([0, 0, 1, 1])

    rounded = array_round(arr)
    assert np.alltrue(rounded == expected)
    

def test_circle_points():
    angle = 180
    num = 3
    radius = 250
    expected = np.array([
        [-radius, 0],
        [0, -radius],
        [radius, 0]
    ])

    points = circle_points(angle, num, radius)

    assert points.shape == (num, 2)
    assert np.alltrue(points == expected) 
