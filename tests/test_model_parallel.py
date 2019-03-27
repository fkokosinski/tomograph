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
    pass
