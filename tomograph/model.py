import abc
import numpy as np
from skimage.io import imread
from skimage.draw import line
from tomograph.transform import translate, rotate, transform_apply
from tomograph.utils import array_round, calc_radius, circle_points


class BaseTomograph(metaclass=abc.ABCMeta):
    """ Abstract computer tomography class. """

    @abc.abstractmethod
    def get_lines(self):
        """ Get beam line from emitter to detector. """

    def scan(self):
        """ Perform a scan in current position of tomograph. """
        scans = []

        for beam_line in self.get_lines():
            if np.sum(self.img[beam_line]) == 0:
                scans.append(0)
            else:
                scans.append(np.mean(self.img[beam_line]))

        return np.array(scans)

    def draw(self, out, count, scans):
        """ Reconstruct the original image in a particular position. """
        for beam_line, scan in zip(self.get_lines(), scans):
            out[beam_line] += scan
            count[beam_line] += 1

    def rotate(self, angle):
        """ Perform tomograph rotation. """
        self.angle += angle

    def __init__(self, emitters, detectors):
        self.emitters = emitters
        self.detectors = detectors
        self.angle = 0


class ConeTomograph(BaseTomograph):
    """ Cone beam tomography implementation of BaseTomograph. """

    def get_lines(self):
        """ Get coordinates that beams are going through. """
        max_x, max_y = self.img.shape

        # get transformations
        mat_t = translate(max_x/2, max_y/2)
        mat_r = rotate(np.deg2rad(self.angle))
        transformations = [mat_r, mat_t]

        # transform
        emitters_t = transform_apply(self.emitters, transformations)
        detectors_t = transform_apply(self.detectors, transformations)

        # round
        emitters_t = array_round(emitters_t)
        detectors_t = array_round(detectors_t)

        # get lines
        lines = []
        emitter = emitters_t[0]
        for detector in detectors_t:
            new_line = np.column_stack(line(*emitter, *detector))
            new_line = new_line[
                    (new_line[:, 0] >= 0) &
                    (new_line[:, 1] >= 0) &
                    (new_line[:, 0] < max_x) &
                    (new_line[:, 1] < max_y)
            ]
            lines.append((new_line[:, 0], new_line[:, 1]))

        return lines

    def __init__(self, img, detectors_num, detectors_angle):
        # read image and calculate radius
        self.img = imread(img, as_gray=True)
        radius = calc_radius(*self.img.shape)

        # calulcate emitter/detector position
        emitters = np.array([[0, radius]])
        detectors = circle_points(detectors_angle,
                                  detectors_num, radius)

        # round
        emitters = array_round(emitters)
        detectors = array_round(detectors)

        super(ConeTomograph, self).__init__(emitters, detectors)


class ParallelTomograph(BaseTomograph):
    """ Parallel beam tomography implementation of BaseTomograph. """

    def get_lines(self):
        """ Get coordinates that beams are going through. """
        max_x, max_y = self.img.shape

        # get transformations
        mat_t = translate(max_x/2, max_y/2)
        mat_r = rotate(self.angle)
        transformations = [mat_r, mat_t]

        # transform
        emitters_t = transform_apply(self.emitters, transformations)
        detectors_t = transform_apply(self.detectors, transformations)

        # round
        emitters_t = array_round(emitters_t)
        detectors_t = array_round(detectors_t)

        # get lines
        lines = []
        for emitter, detector in zip(emitters_t, detectors_t):
            new_line = np.column_stack(line(*emitter, *detector))
            new_line = new_line[
                    (new_line[:, 0] >= 0) &
                    (new_line[:, 1] >= 0) &
                    (new_line[:, 0] < max_x) &
                    (new_line[:, 1] < max_y)
            ]
            lines.append((new_line[:, 0], new_line[:, 1]))

        return lines

    def __init__(self, img, detectors_num, detectors_angle):
        self.img = imread(img, as_gray=True)
        radius = calc_radius(*self.img.shape)

        detectors = circle_points(detectors_angle,
                                  detectors_num, radius)
        emitters = detectors * np.array([1, -1])

        super(ParallelTomograph, self).__init__(emitters, detectors)
