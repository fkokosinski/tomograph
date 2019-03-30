import numpy as np
from tomograph.model import ParallelTomograph


def test_parallel_model_cone():
    # expected results
    expected_emitters = np.array([
        [-362, 0],
        [0, 362],
        [362, 0]
    ])
    expected_detectors = np.array([
        [-362, 0],
        [0, -362],
        [362, 0]
    ])

    image = 'tests/test.jpg'
    detectors_num = 3
    detectors_angle = 180

    tomograph = ParallelTomograph(image, detectors_num, detectors_angle)
    assert tomograph.img.shape == (512, 512)
    assert np.alltrue(tomograph.emitters == expected_emitters)
    assert np.alltrue(tomograph.detectors == expected_detectors)


def test_model_parallel_get_lines():
    image = 'tests/test.bmp'
    detectors_num = 3
    detectors_angle = 60

    line1 = (
        np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1]),
        np.array([9, 8, 7, 6, 5, 4, 3, 2, 1, 0])
    )
    line2 = (
        np.array([5, 5, 5, 5, 5, 5, 5, 5, 5, 5]),
        np.array([9, 8, 7, 6, 5, 4, 3, 2, 1, 0])
    )
    line3 = (
        np.array([9, 9, 9, 9, 9, 9, 9, 9, 9, 9]),
        np.array([9, 8, 7, 6, 5, 4, 3, 2, 1, 0])
    )
    expected = [line1, line2, line3]

    tomograph = ParallelTomograph(image, detectors_num, detectors_angle)
    lines = tomograph.get_lines()

    for i in range(len(expected)):
        x, y = expected[i]
        assert np.alltrue(lines[i][0] == x)
        assert np.alltrue(lines[i][1] == y)
