import sys
import logging
from .core import Simulator

from . import __version__

def main():
    assert sys.version_info >= (3, 8), r'PySDS needs python >= 3.8.\n Run [python --version] for more info.'
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--dl_db_name', help='Deep Learning database name',
                        type=str, default='pysds_dl_db')
    parser.add_argument('-w', '--workspace', help='PySDS Workspace',
                        type=str, default='PySDS_workspace')
    parser.add_argument('-s', '--nsize', help='Number of patches to simulate in the DL database.', 
                        type=int, default=1000)
    parser.add_argument('-d', '--dsize', help='Patch size of the deep learing databse.', 
                        type=int, default=128)
    parser.add_argument('-o', '--overlap', help='Define overlap between patches. Defualt is no overlap.',
                        type=tuple, default=None)
    parser.add_argument('-p', '--soc_path', help='SOC map file path.',
                        type=str, default=None)
    parser.add_argument('-f', '--frequency', help='Frequency of the simulation wave. Default is L-band (1.41 GHz)',
                        type=float, default=float(1.41))
    parser.add_argument('-t', '--sst_range', help='Min, Max, and Step of the Soil Surface Temperature in °C.',
                        nargs=3, type=int, default=(-25, 25, 5))
    parser.add_argument('-m', '--ssm_range', help='Min, Max, and Step of the Soil Surface Moisture in %%.',
                        nargs=3, type=float, default=(0.05, 0.55, 0.1))
    parser.add_argument('-l', '--no_data_threshold', help='No data limit in finding offsets.',
                        type=float, default=float(0.4))
    parser.add_argument('-b', '--max_search_distance', help='The maximum distance (in pixels) that the algorithm will search out for values to interpolate. The default is 10 pixels.',
                        type=float, default=None)
    parser.add_argument('-i', '--smoothing_iterations', help='The number of 3x3 average filter smoothing iterations to run after the interpolation to dampen artifacts. The default is zero smoothing iterations.',
                        type=int, default=None)
    parser.add_argument('-v', '--verbose', help='Provides detailed (DEBUG) logging for ssPss. Default is false',
                        default=False, action='store_true')
    parser.add_argument('--version', action='version', version=__version__)
    
    args = parser.parse_args()

    # TODO Add error skipping
    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logger = Simulator.init_loggers(msg_level=logging_level)

    # Create an instance of the Simulator class
    sim = Simulator(dl_db_name=args.dl_db_name, workspace=args.workspace, dataset_size=args.nsize, patch_size=args.dsize,
                    soc_path=args.soc_path, freq_GHz=args.frequency, sst_range=args.sst_range, ssm_range=args.ssm_range,
                    no_data_threshold=args.no_data_threshold, step=args.overlap, max_search_distance=args.max_search_distance,
                    smoothing_iterations=args.smoothing_iterations, logger=logger)

    # Run the simulation
    sim.run()


if __name__ == '__main__':
    main()