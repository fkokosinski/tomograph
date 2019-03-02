import argparse
import numpy as np
from tomograph import Tomograph
from plot import visualize


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Parametrized parallel tomograph simulator'
    )

    parser.add_argument('image', action='store', help='absolute path to image')
    parser.add_argument('num', action='store', type=int,
                        help='number of emitters/detectors')
    parser.add_argument('span', action='store', type=int,
                        help='emitter/detector span')
    parser.add_argument('rotations', action='store', type=int,
                        help='number of rotations')

    plot_group = parser.add_argument_group('visualize')
    plot_group.add_argument('--steps', action='store', type=int, default=None,
                            help='use pyplot to visualize emitters/detectors \
                            position after n steps instead of generating \
                            sinogram')

    args = parser.parse_args()

    step = 2*np.pi / args.rotations
    tomograph = Tomograph(args.image, args.num, args.span)

    if args.steps is not None:
        visualize(tomograph, step*args.steps)
