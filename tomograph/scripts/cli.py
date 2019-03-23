import click
import numpy as np
from skimage.io import imsave
from tqdm import tqdm
from tomograph.model import ParallelTomograph


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
    step = 360 / rotations

    tomograph = ParallelTomograph(patient, detectors, angle)
    sinogram = []
    reverse = np.zeros(tomograph.img.shape, dtype=np.float64)
    count = np.zeros(tomograph.img.shape, dtype=np.float64)
    kernel = np.array([-2, 5, -2])

    for i in tqdm(range(rotations)):
        tomograph.rotate(step)
        scan = tomograph.scan()
        sinogram.append(np.convolve(scan, kernel))
        tomograph.draw(reverse, count, scan)

    count[np.where(count == 0)] += 1

    out = np.array(sinogram).T
    out[np.where(out < 0.0)] = 0.0
    out[np.where(out > 1.0)] = 1.0

    out_reverse = reverse/count

    imsave(f'{prefix}_radon.bmp', out)
    imsave(f'{prefix}_reverse.bmp', out_reverse)
