# tomograph - paramterized computer tomography simulator

[![Build Status](https://travis-ci.com/fkokosinski/tomograph.svg?token=KqDQHrZxZ4q79UZ1qZJw&branch=master)](https://travis-ci.com/fkokosinski/tomograph) [![codecov](https://codecov.io/gh/fkokosinski/tomograph/branch/master/graph/badge.svg?token=SogoLYXs8u)](https://codecov.io/gh/fkokosinski/tomograph)

`tomograph` is a parametrized computer tomography simulator, which can be run as
a standalone script or included as a module in your Python programs. It
implements both Radon and reverse Radon transforms. It currently models two
types of beam projections: cone and parallel.

## Dependencies
Currently `tomograph` requires:
- Click (`click`)
- tqdm (`tqdm`)
- NumPy (`numpy`)
- Image Processing SciKit (`scikit-image`)

Their respective required versions can be seen in `requirements.txt` file.

## Installation
Simply run:

    pip install tomograph

Tomograph supports Python 3.5, Python 3.6 and Python 3.7.

## Usage
`tomograph` can be used directly through command-line interface or as a Python
module:

### Commandline
Using command-line interface:

    tomograph --model cone --detectors 256 --angle 150 --rotations 512 image.jpg

All command-line arguments can be seen by running:

    tomograph --help

### Module
Example script that does Radon transform using cone beam model:

    from skimage.io import imsave
    from tomograph.model import ConeTomograph

    # variables
    path = 'image.jpg'
    detectors = 256
    angle = 180
    rotations = 512

    # one scan per rotation
    step = 360 / rotations

    # perform Radon transform
    tomograph = ConeTomograph(path, detectors, angle)
    sinogram = []
    for i in range(rotations):
        tomograph.rotate(step)  # rotate tomograph
        scan = tomograph.scan() # do the scan
        sinogram.append(scan)

    imsave('radon.bmp', np.array(sinogram).T)
