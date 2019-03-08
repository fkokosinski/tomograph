import cv2
import numpy as np
from bresenham import bresenham


class Tomograph():
    def coords_to_integer(self):
        self.emitter = np.rint(self.emitter).astype(int)
        self.detectors = np.rint(self.detectors).astype(int)

    def rotate(self, alpha):
        self.alpha += alpha
        rotation_mat = np.array([
            [np.cos(alpha), np.sin(alpha)],
            [-np.sin(alpha), np.cos(alpha)]
        ])

        self.emitter = self.emitter.dot(rotation_mat)
        self.detectors = self.detectors.dot(rotation_mat)
        self.coords_to_integer()

    def scan(self):
        # calculate offset
        shape = self.img.shape
        x_off = round(shape[0]/2)
        y_off = round(shape[1]/2)
        off = np.array([x_off, y_off])

        # apply offset
        emitter = self.emitter + off
        detectors = self.detectors + off

        pairs = []
        for detector in detectors:
            pairs.append((*emitter, *detector))

        lines = [bresenham(*x) for x in pairs]

        scans = []
        for line in lines:
            sum = 0
            filtered = [x for x in line if x[0] >= 0 and x[1] >= 0]
            filtered = [
                    x for x in filtered if x[0] < shape[0] and x[1] < shape[1]
            ]

            for x, y in filtered:
                sum += self.img[x, y]

            if sum > 0:
                sum /= len(filtered)

            scans.append(sum)

        return scans

    def draw(self, img, count, values):
        # calculate offset
        shape = self.img.shape
        x_off = round(shape[0]/2)
        y_off = round(shape[1]/2)
        off = np.array([x_off, y_off])

        # apply offset
        emitter = self.emitter + off
        detectors = self.detectors + off

        pairs = []
        for detector in detectors:
            pairs.append((*emitter, *detector))

        lines = [bresenham(*x) for x in pairs]

        scans = []
        for line, value in zip(lines, values):
            filtered = [x for x in line if x[0] >= 0 and x[1] >= 0]
            filtered = [
                    x for x in filtered if x[0] < shape[0] and x[1] < shape[1]
            ]

            for x, y in filtered:
                img[x, y] += value
                count[x, y] += 1

    def __init__(self, imgpath, num, span):
        self.detectors = []

        # rotation from base position
        self.alpha = 0.0

        # our patient
        self.img = cv2.imread(imgpath, cv2.IMREAD_GRAYSCALE)

        # calculate tomograph's radius
        shape = self.img.shape
        self.radius = np.sqrt(shape[0]**2 + shape[1]**2)/2

        # emitter coord
        self.emitter = np.array([0, -self.radius])

        # detectors coords
        sample_detector = np.array([0, self.radius])
        span = np.deg2rad(span)
        for alpha in np.linspace(-span/2, span/2, num=num):
            rotation_mat = np.array([
                [np.cos(alpha), np.sin(alpha)],
                [-np.sin(alpha), np.cos(alpha)]
            ])
            self.detectors.append(sample_detector.dot(rotation_mat))

        self.coords_to_integer()
