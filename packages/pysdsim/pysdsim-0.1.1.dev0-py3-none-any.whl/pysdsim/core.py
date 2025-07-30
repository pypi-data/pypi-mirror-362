import os
import sys
import random
import string
import logging
import rasterio
import itertools
import numpy as np
import tables as tb
from tdmrsdm import TDMRSDM
from rasterio.fill import fillnodata
from numpy.lib.stride_tricks import sliding_window_view




class Simulator:


    def __init__(self, workspace:str, dataset_size:int, patch_size:tuple, soc_path:str, 
                 freq_GHz:float, sst_range:tuple, ssm_range:tuple, no_data_threshold:float,
                 step:tuple, max_search_distance:int, smoothing_iterations:int, **kwargs):
        
        self.logger = kwargs.get("logger", logging.getLogger("root"))
        self.logger.info("============= This is PySDS version: %s ==============" % self._get_version())
        
        # assign parameters
        self.workspace = workspace
        self.f = freq_GHz
        self.sst_range = sst_range
        self.ssm_range = ssm_range
        self.nsize = dataset_size
        self.patch_size = (patch_size, patch_size)
        self.step = step
        self.max_search_distance = max_search_distance
        self.smoothing_iterations = smoothing_iterations
        self.no_data_threshold = no_data_threshold
        self.soc_path = soc_path

        return None

    def _get_version(self):
        from . import __version__
        return __version__
    
    @staticmethod
    def init_loggers(msg_level=logging.DEBUG):
        """
        Init a stdout logger
        :param msg_level: Standard msgLevel for both loggers. Default is DEBUG
        """

        logging.getLogger().addHandler(logging.NullHandler())
        # Create default path or get the pathname without the extension, if there is one
        logger = logging.getLogger("root")
        logger.handlers = []  # Remove the standard handler again - Bug in logging module

        logger.setLevel(msg_level)
        formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s")

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def run(self):
        if self._in_colab_shell():
            local_out_dir = os.path.join('/content/drive/MyDrive', self.workspace)
        else:
            local_out_dir = os.path.join(os.path.expanduser('~'), self.workspace)
        
        if not os.path.exists(local_out_dir):
            # Create a new directory because it does not exist
            os.makedirs(local_out_dir)
            self.logger.info(f'The workspace directory is created!')
        
        # create a str var from sst_range and ssm_range
        sst_range_str = '_'.join(map(str, self.sst_range))
        ssm_range_str = '_'.join(map(str, self.ssm_range))

        dl_db_name = f'SDC_DP_DB_n{self.nsize}_p{self.patch_size[0]}_f{self.f}_sst{sst_range_str}_ssm{ssm_range_str}.npz'

        self.logger.info(rf'Workspace directory: {local_out_dir}')
        self.logger.info(rf'Soil dielectric database name: {dl_db_name}')
        
        self._execute(local_out_dir, dl_db_name)
        
        return None
    
    def _execute(self, out_dir, dbname):
    
        # Define outfile directory
        outfilename = os.path.join(out_dir, dbname)
    
        patches = self._extract_patches(
            patch_size=self.patch_size, step=self.step, soc_path=self.soc_path, 
            max_search_distance=self.max_search_distance, 
            smoothing_iterations=self.smoothing_iterations, 
            no_data_threshold=self.no_data_threshold
        )
        
        self.logger.info(f'Found {len(patches)} patches with size of {self.patch_size} to process.')

        from collections import defaultdict
        data_dict = defaultdict(lambda: None)

        # Load existing data if the file exists
        if os.path.exists(outfilename):
            data_dict.update(np.load(outfilename))
            self.logger.info(f"Loaded existing data from {outfilename}")

        for n, soc in enumerate(patches[:self.nsize]):
            som = self._to_som(soc) / 10.       # SOM (%)
            sbd = self._pedoTransferSBD(soc)    # soil bulk dry density g/cm^3
            ssts = np.arange(*self.sst_range)
            mvs = np.arange(*self.ssm_range)

            self.logger.debug(f'Number of permutations: {len(ssts) * len(mvs)} for patch {n+1}/{len(patches)}')
            eps_list = []
            for st, mv in itertools.product(ssts, mvs):
                mrsdm = TDMRSDM(freq_GHz=self.f, sst=st, som=som, sbd=sbd, ssm=mv)
                eps_list.append(mrsdm.run())
            eps_array = np.stack(eps_list)
            patch_key = f"patch_{n:04d}"
            data_dict[patch_key] = eps_array
            self.logger.debug(f"Processed patch {n+1}/{len(patches)} ('{patch_key}') and added to in-memory dictionary.")
        
        # Save all data at once
        np.savez(outfilename, **data_dict)
        self.logger.info(f"Simulation of soil dielectric properties has been successfully completed. All data saved to {outfilename}.")
        
        return None
    
    def _in_colab_shell(self,):
        """Tests if the code is being executed within Google Colab."""
        import sys

        if "google.colab" in sys.modules:
            return True
        else:
            return False
    
    def _to_som(self, soc):
        return soc * 1.724

    def _pedoTransferSBD(self, soc):
        return 1.3770 * np.exp(-0.048 * soc)

    def _get_random_name(self, length):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        name = ''.join(random.choice(letters) for i in range(length))

        return name
    
    def _extract_patches(self, patch_size, step, soc_path, max_search_distance, smoothing_iterations, no_data_threshold):

        # Unpack patch dimensions
        patch_h, patch_w = patch_size
        # Default to non-overlapping if no step provided
        step_h, step_w = step if step is not None else patch_size

        # Read raster and fill no-data
        with rasterio.open(soc_path) as src:
            data = src.read(1)  # assume band 1 fits in memory

        # Mask valid (non-NaN) pixels and fill others
        valid_mask = ~np.isnan(data)
        if not valid_mask.any():
            raise ValueError("No valid data found in the SOC map.")
        
        # if max_search_distance and smoothing_iterations not set ignore fillnodata
        if max_search_distance is not None or smoothing_iterations is not None:
            self.logger.info(f"Filling NaN values in SOC map with max search distance {max_search_distance} and smoothing iterations {smoothing_iterations}.")

            # Fill NaN values using rasterio's fillnodata
            filled = fillnodata(data, mask=valid_mask, max_search_distance=max_search_distance,
                            smoothing_iterations=smoothing_iterations)
        else:
            self.logger.info("Skipping fillnodata as max_search_distance or smoothing_iterations is not set.")
            filled = data
        
        # Create a view of all sliding windows, then subsample by step
        windows = sliding_window_view(filled, window_shape=(patch_h, patch_w))
        sampled = windows[::step_h, ::step_w]

        # Flatten into (num_patches, patch_h, patch_w)
        num_rows, num_cols, _, _ = sampled.shape
        patches = sampled.reshape(num_rows * num_cols, patch_h, patch_w)

        # If filtering by NaN ratio, compute per-patch and mask
        if no_data_threshold >= 0.0:
            total_pixels = patch_h * patch_w
            # count NaNs in each patch
            nan_counts = np.isnan(patches).sum(axis=(1, 2))
            keep_mask = nan_counts <= (no_data_threshold * total_pixels)
            patches = patches[keep_mask]

        return patches
    
