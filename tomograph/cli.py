import click
import numpy as np
from skimage.io import imsave
from tqdm import tqdm
from tomograph.model import ConeTomograph, ParallelTomograph


tomograph_switch = {
        'cone': ConeTomograph,
        'parallel': ParallelTomograph
}


@click.command()
@click.option('--model', type=click.Choice(['cone', 'parallel']),
              required=True, help='Model of beams used in tomography')
@click.option('--detectors', required=True, type=int,
              help='Number of detectors')
@click.option('--angle', required=True, type=float,
              help='Angle between outermost detectors in degrees')
@click.option('--rotations', required=True, type=int,
              help='Number of rotations in a full scan')
@click.option('--prefix', default='out', type=str,
              help='Prefix of output file names')
@click.argument('patient')
def main(model, detectors, angle, rotations, prefix, patient):
    """ Parametrized computer tomography simulator """
    step = 360 / rotations

    # get tomography type
    tomograph_type = tomograph_switch.get(model)
    tomograph = tomograph_type(patient, detectors, angle)

    # initialize needed structures
    sinogram = []
    reverse = np.zeros(tomograph.img.shape, dtype=np.float64)
    count = np.zeros(tomograph.img.shape, dtype=np.float64)

    for i in tqdm(range(rotations)):
        tomograph.rotate(step)
        scan = tomograph.scan()
        sinogram.append(scan)
        tomograph.draw(reverse, count, scan)

    count[np.where(count == 0)] += 1

    out = np.array(sinogram).T
    out[np.where(out < 0.0)] = 0.0
    out[np.where(out > 1.0)] = 1.0

    out_reverse = reverse/count
    out_reverse /= np.amax(out_reverse) + 0.25

    imsave('{}_radon.bmp'.format(prefix), out)
    imsave('{}_reverse.bmp'.format(prefix), out_reverse)
