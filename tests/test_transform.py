import numpy as np
from tomograph.transform import projective, cartesian, translate, rotate
from tomograph.transform import transform_list, transform_apply


def test_transform_projective():
    """ Test tomograph.transform.projective convertion. """
    coords = np.linspace(0, 9, num=10).reshape(5, 2)
    expected = np.array([
        [0.0, 1.0, 1.0],
        [2.0, 3.0, 1.0],
        [4.0, 5.0, 1.0],
        [6.0, 7.0, 1.0],
        [8.0, 9.0, 1.0],
    ])

    coords = projective(coords)
    assert np.allclose(coords, expected)


def test_transform_cartesian():
    """ Test tomograph.transform.cartesian convertion. """
    coords = np.array([
        [0.0, 1.0, 1.0],
        [2.0, 3.0, 1.0],
        [4.0, 5.0, 1.0],
        [6.0, 7.0, 1.0],
        [8.0, 9.0, 1.0],
    ])
    expected = np.linspace(0, 9, num=10).reshape(5, 2)

    coords = cartesian(coords)
    assert np.allclose(coords, expected)


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
    expected = np.array([-50.0, 100.0, 1.0])

    coords = rotate(angle).dot(coords)
    assert np.allclose(coords, expected)


def test_transform_join():
    """ Test joining two transform matrices. """
    coords = np.array([-100, 50, 1])
    move = (-150, 125)
    angle = np.pi / 2
    expected = np.array([-200.0, 25.0, 1.0])

    coords = rotate(angle).dot(coords)
    coords = translate(*move).dot(coords)
    assert np.allclose(coords, expected)


def test_transform_list():
    """ Test transforming a list of coordinates. """
    coords = np.linspace(10, 100, num=10).reshape(5, 2)
    w = np.array([[1], ]*5)
    coords = np.append(coords, w, axis=1)
    t_mat = translate(100, 50)
    expected = coords + np.array([100, 50, 0])

    coords = transform_list(coords, t_mat)
    assert np.allclose(coords, expected)


def test_transform_apply():
    """ Test applying list of transformations to a list of coordinates. """
    coords = np.linspace(10, 100, num=10).reshape(5, 2)
    w = np.array([[1], ]*5)
    coords = np.append(coords, w, axis=1)
    expected = np.array([
        [90, 30, 1],
        [70, 10, 1],
        [50, -10, 1],
        [30, -30, 1],
        [10, -50, 1]
    ])

    t_mat = translate(100, 50)
    r_mat = rotate(np.pi)

    # rotate first, then translate
    transformations = [t_mat, r_mat]

    coords = transform_apply(coords, transformations)
    assert np.allclose(coords, expected)
