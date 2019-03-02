import cv2
import numpy as np


class Tomograph():
    def __init__(self, imgpath, num, span):
        self.alpha = 0.0
        self.img = cv2.imread(imgpath, cv2.IMREAD_GRAYSCALE)

        shape = self.img.shape
        self.radius = np.sqrt(shape[0]**2 + shape[1]**2)/2

        self.emitters = np.array(
                [(x, self.radius) for x in np.linspace(-span/2,
                                                       span/2,
                                                       num=num)]
        )
        self.detectors = np.array(
                [(x, -self.radius) for x in np.linspace(-span/2,
                                                        span/2,
                                                        num=num)]
        )

    def rotate(self, alpha):
        self.alpha += alpha
        rotation_mat = np.array([
            [np.cos(alpha), np.sin(alpha)],
            [-np.sin(alpha), np.cos(alpha)]
        ])

        self.emitters = self.emitters.dot(rotation_mat)
        self.detectors = self.detectors.dot(rotation_mat)
