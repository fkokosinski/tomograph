import numpy as np
from tomograph.model import BaseTomograph


class DummyTomograph(BaseTomograph):
    def get_lines(self):
        lines = []

        # first line
        x = np.linspace(0, 9, num=10, dtype=int)
        line = (x, x)
        lines.append(line)

        # second line
        x = np.zeros(10, dtype=int)
        y = np.linspace(0, 9, num=10, dtype=int)
        line = (x, y)
        lines.append(line)

        return lines

    def __init__(self, emitters, detectors):
        super(DummyTomograph, self).__init__(emitters, detectors)


def test_model_base_tomograph():
    detectors = np.array([
        [1, 2],
        [3, 4],
        [5, 6]
    ])
    emitters = np.array([
        [10, 20],
        [30, 40]
    ])
    tomograph = DummyTomograph(emitters, detectors)

    assert np.alltrue(tomograph.emitters == emitters)
    assert np.alltrue(tomograph.detectors == detectors)
    assert tomograph.angle == 0


def test_model_base_tomograph_rotate():
    detectors = np.array([
        [1, 2],
        [3, 4],
        [5, 6]
    ])
    emitters = np.array([
        [10, 20],
        [30, 40]
    ])
    tomograph = DummyTomograph(emitters, detectors)

    tomograph.rotate(34)
    tomograph.rotate(-12)
    assert tomograph.angle == 22


def test_model_base_tomograph_scan():
    expected = np.array([0.4, 0.0])

    # not really needed, only for tomograph constructor
    detectors = np.array([])
    emitters = np.array([])

    # prepare dummy image
    image = np.zeros((10, 10))
    image[3:7, 3:7] = 1.0

    tomograph = DummyTomograph(emitters, detectors)
    tomograph.img = image

    scan = tomograph.scan()
    assert np.allclose(scan, expected)


def test_model_base_tomograph_draw():
    x = np.linspace(0, 9, num=10, dtype=int)
    expected_out = np.zeros((10, 10))
    expected_count = np.zeros((10, 10))
    expected_out[x, x] = 0.67
    expected_count[x, x] += 1
    expected_count[0, x] += 1

    # not really needed, only for tomograph constructor
    detectors = np.array([])
    emitters = np.array([])
    scans = np.array([0.67, 0.0])

    # prepare arrays
    out = np.zeros((10, 10))
    count = np.zeros((10, 10))

    tomograph = DummyTomograph(emitters, detectors)
    tomograph.draw(out, count, scans)
    assert np.allclose(out, expected_out)
    assert np.alltrue(count == expected_count)
