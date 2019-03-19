import click
import cv2
import numpy as np
from tqdm import tqdm
from tomograph import Tomograph


@click.command()
@click.option('--detectors', required=True, type=int,
              help='Number of detectors')
@click.option('--angle', required=True, type=float,
              help='Angle between outermost detectors in degrees')
@click.option('--rotations', required=True, type=int,
              help='Number of rotations in a full scan')
@click.option('--prefix', default='out', type=str,
              help='Prefix of output file names')
@click.argument('patient')
def main(detectors, angle, rotations, prefix, patient):
    """ Parametrized cone beam tomography simulator """
    step = 2*np.pi / rotations
    tomograph = Tomograph(patient, detectors, angle)

    sinogram = []
    reverse = np.zeros(tomograph.img.shape, dtype=int)
    count = np.zeros(tomograph.img.shape, dtype=int)

    for i in tqdm(range(rotations)):
        tomograph.rotate(step)
        sinogram.append(tomograph.scan())
        tomograph.draw(reverse, count, np.array(sinogram).T[:, i])

    sinogram = np.array(sinogram)
    sinogram = np.rint(sinogram)
    sinogram = sinogram.astype(int)
    count[np.where(count == 0)] += 1

    cv2.imwrite(f'{prefix}_radon.bmp', 3*sinogram.T)
    cv2.imwrite(f'{prefix}_reverse.bmp', reverse/count)


if __name__ == '__main__':
    main()
