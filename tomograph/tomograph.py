import cv2
import numpy as np
from bresenham import bresenham


class Tomograph():
    def coords_to_integer(self):
        # round to the nearest integer
        self.emitters = np.rint(self.emitters)
        self.detectors = np.rint(self.detectors)

        # convert to integers
        self.emitters = self.emitters.astype(int)
        self.detectors = self.detectors.astype(int)

    def rotate(self, alpha):
        self.alpha += alpha
        rotation_mat = np.array([
            [np.cos(alpha), np.sin(alpha)],
            [-np.sin(alpha), np.cos(alpha)]
        ])

        self.emitters = self.emitters.dot(rotation_mat)
        self.detectors = self.detectors.dot(rotation_mat)
        self.coords_to_integer()

    def scan(self):
        # calculate offset
        shape = self.img.shape
        x_off = round(shape[0]/2)
        y_off = round(shape[1]/2)
        off = np.array([x_off, y_off])

        # apply offset
        emitters = self.emitters + off
        detectors = self.detectors + off

        pairs = []
        for pair in zip(emitters, detectors):
            pairs.append([*pair[0], *pair[1]])

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

            sum /= len(filtered)
            scans.append(sum)

        return scans

    def __init__(self, imgpath, num, span):
        self.emitters = []
        self.detectors = []

        # rotation from base position
        self.alpha = 0.0

        # our patient
        self.img = cv2.imread(imgpath, cv2.IMREAD_GRAYSCALE)

        # calculate tomograph's radius
        shape = self.img.shape
        self.radius = np.sqrt(shape[0]**2 + shape[1]**2)/2

        # calculate emitters/detecors coords
        for x in np.linspace(-span/2, span/2, num=num):
            self.emitters.append((x, self.radius))
            self.detectors.append((x, -self.radius))

        self.coords_to_integer()
