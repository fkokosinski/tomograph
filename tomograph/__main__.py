import argparse
import numpy as np
import cv2
from tomograph import Tomograph


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Parametrized cone tomograph simulator'
    )

    parser.add_argument('action', action='store', help='scan/draw image')
    parser.add_argument('image', action='store', help='absolute path to image')
    parser.add_argument('num', action='store', type=int,
                        help='number of detectors')
    parser.add_argument('span', action='store', type=int,
                        help='emitter/detector span')
    parser.add_argument('rotations', action='store', type=int,
                        help='number of rotations')
    parser.add_argument('out', action='store', help='output path')

    args = parser.parse_args()

    step = 2*np.pi / args.rotations
    tomograph = Tomograph(args.image, args.num, args.span)

    if args.action == 'scan':
        sinogram = []
        for i in range(args.rotations):
            tomograph.rotate(step)
            sinogram.append(tomograph.scan())

        sinogram = np.array(sinogram)
        sinogram = np.rint(sinogram)
        sinogram = sinogram.astype(int)

        cv2.imwrite(args.out, 3*sinogram.T)
    elif args.action == 'draw':
        radon = cv2.imread(args.image, cv2.IMREAD_GRAYSCALE)
        reverse = np.zeros(radon.shape, dtype=int)
        count = np.zeros(radon.shape, dtype=int)

        for i in range(args.rotations):
            tomograph.rotate(step)
            tomograph.draw(reverse, count, radon[:, i])

        count[np.where(count == 0)] += 1
        cv2.imwrite(args.out, reverse/count)

        # filtering
        ker = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ])
        filtered = reverse/count
        out = np.empty(filtered.shape)

        print("filtering...")
        for x in range(1, filtered.shape[0]-1):
            for y in range(1, filtered.shape[1]-1):
                out[x-1, y-1] = np.sum(ker * filtered[x-1:x+2, y-1:y+2])

        cv2.imwrite('filtered.bmp', out)
