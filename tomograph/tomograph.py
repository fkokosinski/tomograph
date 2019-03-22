import abc
import numpy as np
from skimage.io import imread
from skimage.draw import line
import utils


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

    def draw(self, img, count, scans):
        """ Reconstruct the original image in a particular position. """
        pass

    def rotate(self, angle):
        """ Perform tomograph rotation. """
        # convert to radians
        alpha = np.deg2rad(angle)

        # get rotation matrix
        rotation_mat = np.array([
            [np.cos(alpha), np.sin(alpha)],
            [-np.sin(alpha), np.cos(alpha)]
        ])

        # apply transformation to emitter/detector coords
        self.emitters = utils.array_round(self.emitters.dot(rotation_mat))
        self.detectors = utils.array_round(self.detectors.dot(rotation_mat))

    def __init__(self, emitters, detectors):
        self.emitters = emitters
        self.detectors = detectors


class ConeTomograph(BaseTomograph):
    """ Cone beam tomography implementation of BaseTomograph. """

    def get_lines(self):
        """ Get coordinates that beams are going through. """
        max_x, max_y = self.img.shape

        # get offset
        move = np.array(self.img.shape)
        move = np.rint(move/2).astype(int)

        # move emitter/detector coordinates
        moved_emitter = self.emitters + move
        moved_detectors = self.detectors + move

        # get lines
        lines = []
        for detector in moved_detectors:
            new_line = np.column_stack(line(*moved_emitter, *detector))
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
        radius = utils.calc_radius(*self.img.shape)

        # calulcate emitter/detector position
        emitters = np.array([0, radius])
        detectors = utils.circle_points(detectors_angle,
                                        detectors_num, radius)

        # round
        emitters = utils.array_round(emitters)
        detectors = utils.array_round(detectors)

        super(ConeTomograph, self).__init__(emitters, detectors)
