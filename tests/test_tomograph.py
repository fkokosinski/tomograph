import numpy as np
from tomograph.model import ConeTomograph


def test_tomograph_create():
    img = 'tests/test.jpg'
    num = 3
    angle = 180
    emitter_expected = np.array([0, 362])
    detectors_expected = np.array([
        [-362, 0],
        [0, -362],
        [362, 0]
    ])

    tomograph = ConeTomograph(img, num, angle)

    assert np.alltrue(tomograph.emitters == emitter_expected)
    assert np.alltrue(tomograph.detectors == detectors_expected)


def test_tomograph_rotate():
    img = 'tests/test.jpg'
    num = 3
    angle = 180
    tomograph = ConeTomograph(img, num, angle)
    emitter_expected = np.array([-362, 0])
    detectors_expected = np.array([
        [0, -362],
        [362, 0],
        [0, 362]
    ])

    tomograph.rotate(90)

    assert np.alltrue(tomograph.emitters == emitter_expected)
    assert np.alltrue(tomograph.detectors == detectors_expected)
