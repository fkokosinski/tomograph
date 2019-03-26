import numpy as np
from tomograph.transform import translate, rotate


def test_transform_translate():
    """ Test tomograph.transform.translate translation matrix. """
    coords = np.array([100, 50, 1])
    move = (150, 70)
    expected = np.array([250, 120, 1])

    coords = translate(*move).dot(coords)
    assert np.alltrue(coords == expected)


def test_transform_rotate():
    """ Test tomograph.transform.rotate rotation matrix. """
    coords = np.array([100, 50, 1])
    angle = np.pi / 2
    expected = np.array([50.0, -100.0, 1.0])

    coords = rotate(angle).dot(coords)
    assert np.allclose(coords, expected)


def test_transform_join():
    """ Test joining two transform matrices. """
    coords = np.array([-100, 50, 1])
    move = (-150, 125)
    angle = np.pi / 2
    expected = np.array([-100.0, 225.0, 1.0])

    coords = rotate(angle).dot(coords)
    coords = translate(*move).dot(coords)
    assert np.allclose(coords, expected)
