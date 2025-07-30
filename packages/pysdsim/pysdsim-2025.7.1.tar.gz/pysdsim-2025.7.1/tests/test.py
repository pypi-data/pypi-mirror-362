import unittest
import os
import shutil
import logging
import sys
from unittest.mock import patch, MagicMock # Import mock for testing _in_colab_shell
import numpy as np
import rasterio
import tables as tb
from rasterio.transform import from_origin

# Assuming core.py is in src/pysds relative to the project root
# Adjust the import path if your structure is different
try:
    from src.pysdsim.core import Simulator
except ImportError:
    # If running tests from within the tests directory, adjust path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from src.pysdsim.core import Simulator


class TestSimulator(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures, if any."""
        self.base_workspace = 'test_sim_workspace_dir'
        self.workspace_name = 'test_workspace'
        self.full_workspace_path = os.path.join(os.path.expanduser('~'), self.base_workspace, self.workspace_name, Simulator.OUT_DIR)
        self.dataset_size = 2 # Keep small for testing
        self.patch_size = (32, 32)
        self.soc_path = 'test_soc.tif'
        self.freq_GHz = 1.41
        self.sst_range = (-10, 11, 10) # Use step for arange
        self.ssm_range = (0.1, 0.51, 0.2) # Use step for arange
        self.no_data_limit = 0.5
        self.logger = Simulator.init_loggers(msg_level=logging.ERROR) # Use ERROR to avoid verbose test output

        # --- Create a dummy SOC file for testing ---
        # Ensure the directory for the dummy file exists if it's not the current dir
        soc_dir = os.path.dirname(self.soc_path)
        if soc_dir and not os.path.exists(soc_dir):
            os.makedirs(soc_dir)

        # Create a dummy SOC raster file with some NaNs
        self.raster_rows, self.raster_cols = 128, 128
        dummy_soc_data = np.random.rand(self.raster_rows, self.raster_cols).astype(np.float32) * 10
        # Add some NaN values
        nan_indices = np.random.choice(self.raster_rows * self.raster_cols, size=int(0.1 * self.raster_rows * self.raster_cols), replace=False)
        dummy_soc_data.flat[nan_indices] = np.nan

        profile = {
            'driver': 'GTiff',
            'height': self.raster_rows,
            'width': self.raster_cols,
            'count': 1,
            'dtype': dummy_soc_data.dtype,
            'crs': 'EPSG:4326',
            'transform': from_origin(0, 90, 1, 1), # Dummy transform
            'nodata': np.nan # Explicitly set nodata value
        }

        with rasterio.open(self.soc_path, 'w', **profile) as dst:
            dst.write(dummy_soc_data, 1)
        # --- End of dummy SOC file creation ---

        # Clean up any potential leftover workspace from previous failed runs
        if os.path.exists(self.full_workspace_path):
            shutil.rmtree(self.full_workspace_path)
        # Ensure the base directory exists for creating the workspace
        base_dir = os.path.dirname(self.full_workspace_path)
        if not os.path.exists(base_dir):
             os.makedirs(base_dir)


    def tearDown(self):
        """Tear down test fixtures, if any."""
        # Clean up the workspace after testing
        workspace_parent_dir = os.path.join(os.path.expanduser('~'), self.base_workspace)
        if os.path.exists(workspace_parent_dir):
            shutil.rmtree(workspace_parent_dir)
        # Clean up the dummy SOC file
        if os.path.exists(self.soc_path):
            os.remove(self.soc_path)
        # Clean up potential HDF5 file outside workspace if path logic changes
        sst_range_str = '_'.join(map(str, self.sst_range))
        ssm_range_str = '_'.join(map(str, self.ssm_range))
        h5_name = f'SDC_DP_DB_{self.workspace_name}_n{self.dataset_size}_{self.patch_size[0]}_FGHz{self.freq_GHz}_SST{sst_range_str}_SSM{ssm_range_str}.h5'
        h5_path = os.path.join(self.full_workspace_path, h5_name)
        if os.path.exists(h5_path):
             # This should be covered by workspace cleanup, but good to be explicit
             try:
                 os.remove(h5_path)
             except OSError:
                 pass # May have already been removed by rmtree

    def test_init_creates_workspace_and_sets_attributes(self):
        """Test if __init__ creates the workspace directory and sets attributes."""
        # Mock _run to prevent actual simulation during init test
        with patch.object(Simulator, '_run', return_value=None) as mock_run:
            sim = Simulator(
                workspace=os.path.join(self.base_workspace, self.workspace_name),
                dataset_size=self.dataset_size,
                patch_size=self.patch_size,
                soc_path=self.soc_path,
                freq_GHz=self.freq_GHz,
                sst_range=self.sst_range,
                ssm_range=self.ssm_range,
                no_data_limit=self.no_data_limit,
                logger=self.logger
            )
            self.assertTrue(os.path.exists(self.full_workspace_path))
            self.assertEqual(sim.nsize, self.dataset_size)
            self.assertEqual(sim.size, self.patch_size)
            self.assertEqual(sim.f, self.freq_GHz)
            self.assertEqual(sim.sst_range, self.sst_range)
            self.assertEqual(sim.ssm_range, self.ssm_range)
            self.assertEqual(sim.no_data_limit, self.no_data_limit)
            mock_run.assert_called_once() # Check if _run was called

    def test_init_soc_not_found(self):
        """Test __init__ behavior when SOC file doesn't exist."""
        non_existent_soc = "non_existent_soc.tif"
        # Ensure it doesn't exist
        if os.path.exists(non_existent_soc):
            os.remove(non_existent_soc)

        with patch.object(Simulator, '_run') as mock_run: # Mock _run
            with self.assertLogs(self.logger.name, level='INFO') as log_cm:
                 Simulator(
                    workspace=os.path.join(self.base_workspace, self.workspace_name),
                    dataset_size=self.dataset_size,
                    patch_size=self.patch_size,
                    soc_path=non_existent_soc, # Use non-existent path
                    freq_GHz=self.freq_GHz,
                    sst_range=self.sst_range,
                    ssm_range=self.ssm_range,
                    no_data_limit=self.no_data_limit,
                    logger=self.logger
                )
            # Check if the specific log message is present
            self.assertTrue(any('The required SOC image is not found!' in msg for msg in log_cm.output))
            # Check that _run was NOT called
            mock_run.assert_not_called()


    @patch('sys.modules')
    def test_in_colab_shell(self, mock_sys_modules):
        """Test the _in_colab_shell method."""
        sim = Simulator # Need an instance or class to call the method
        # Test when 'google.colab' is in sys.modules
        mock_sys_modules.__contains__.return_value = True
        self.assertTrue(sim._in_colab_shell(sim)) # Pass dummy self

        # Test when 'google.colab' is NOT in sys.modules
        mock_sys_modules.__contains__.return_value = False
        self.assertFalse(sim._in_colab_shell(sim)) # Pass dummy self

    def test_to_som(self):
        """Test the SOC to SOM conversion."""
        sim = Simulator # Need an instance or class to call the method
        soc_value = 10.0
        expected_som = soc_value * 1.724
        self.assertAlmostEqual(sim._to_som(sim, soc_value), expected_som) # Pass dummy self
        # Test with numpy array
        soc_array = np.array([5.0, 10.0, 15.0])
        expected_som_array = soc_array * 1.724
        np.testing.assert_array_almost_equal(sim._to_som(sim, soc_array), expected_som_array) # Pass dummy self

    def test_pedoTransferSBD(self):
        """Test the pedo transfer function for SBD."""
        sim = Simulator # Need an instance or class to call the method
        soc_value = 5.0
        expected_sbd = 1.3770 * np.exp(-0.048 * soc_value)
        self.assertAlmostEqual(sim._pedoTransferSBD(sim, soc_value), expected_sbd) # Pass dummy self
        # Test with numpy array
        soc_array = np.array([2.0, 5.0, 8.0])
        expected_sbd_array = 1.3770 * np.exp(-0.048 * soc_array)
        np.testing.assert_array_almost_equal(sim._pedoTransferSBD(sim, soc_array), expected_sbd_array) # Pass dummy self

    def test_get_random_name(self):
        """Test random name generation."""
        sim = Simulator # Need an instance or class to call the method
        name_length = 8
        random_name = sim._get_random_name(sim, name_length) # Pass dummy self
        self.assertEqual(len(random_name), name_length)
        self.assertTrue(all(c.islower() and c.isalpha() for c in random_name))

    def test_extract_patches(self):
        """Test patch extraction logic."""
        # Use the static method directly for easier testing
        patch_size = (32, 32)
        step = (16, 16) # Overlapping patches
        nan_threshold = 0.1 # Allow up to 10% NaN

        patches = Simulator._extract_patches(
            raster_path=self.soc_path,
            patch_size=patch_size,
            step=step,
            nan_threshold=nan_threshold,
            max_search_distance=10,
            smoothing_iterations=0
        )

        self.assertIsInstance(patches, np.ndarray)
        self.assertEqual(patches.ndim, 3) # (num_patches, height, width)
        self.assertEqual(patches.shape[1], patch_size[0])
        self.assertEqual(patches.shape[2], patch_size[1])
        self.assertTrue(patches.shape[0] > 0) # Should find some patches

        # Check NaN filtering - difficult to be exact without knowing exact NaN positions
        # but we can check if *some* patches were potentially filtered
        # Calculate max possible patches without filtering
        with rasterio.open(self.soc_path) as src:
            h, w = src.height, src.width
        max_rows = (h - patch_size[0]) // step[0] + 1
        max_cols = (w - patch_size[1]) // step[1] + 1
        max_possible_patches = max_rows * max_cols

        self.assertTrue(patches.shape[0] <= max_possible_patches)
        # We could add a check here that if nan_threshold was 0.0, fewer patches might be returned
        # compared to a high threshold, but this depends heavily on the random NaN placement.

        # Test no-overlap case
        step_no_overlap = patch_size
        patches_no_overlap = Simulator._extract_patches(
            raster_path=self.soc_path,
            patch_size=patch_size,
            step=step_no_overlap, # Use patch size as step
            nan_threshold=nan_threshold
        )
        expected_rows = (self.raster_rows - patch_size[0]) // step_no_overlap[0] + 1
        expected_cols = (self.raster_cols - patch_size[1]) // step_no_overlap[1] + 1
        # The number of patches should be less than or equal to this, due to NaN filtering
        self.assertTrue(patches_no_overlap.shape[0] <= expected_rows * expected_cols)


    @patch('src.pysds.core.TDMRSDM') # Mock the external TDMRSDM class
    def test_run_and_simulate_creates_h5(self, mock_tdmrsdm_class):
        """Test the _run and _simulate methods create HDF5 and add data."""

        # Configure the mock TDMRSDM instance and its run method
        mock_mrsdm_instance = MagicMock()
        # Return a complex numpy array matching patch size
        dummy_eps_output = np.ones(self.patch_size, dtype=np.complex64) * (10 + 5j)
        mock_mrsdm_instance.run.return_value = dummy_eps_output
        mock_tdmrsdm_class.return_value = mock_mrsdm_instance

        # --- Run the simulation ---
        sim = Simulator(
            workspace=os.path.join(self.base_workspace, self.workspace_name),
            dataset_size=self.dataset_size, # Use the small size from setUp
            patch_size=self.patch_size,
            soc_path=self.soc_path,
            freq_GHz=self.freq_GHz,
            sst_range=self.sst_range,
            ssm_range=self.ssm_range,
            no_data_limit=self.no_data_limit,
            logger=self.logger
        )
        # --- Simulation finished ---

        # Define expected HDF5 file path
        sst_range_str = '_'.join(map(str, self.sst_range))
        ssm_range_str = '_'.join(map(str, self.ssm_range))
        h5_name = f'SDC_DP_DB_{self.workspace_name}_n{self.dataset_size}_{self.patch_size[0]}_FGHz{self.freq_GHz}_SST{sst_range_str}_SSM{ssm_range_str}.h5'
        h5_path = os.path.join(self.full_workspace_path, h5_name)

        # 1. Check if HDF5 file was created
        self.assertTrue(os.path.exists(h5_path))

        # 2. Check HDF5 structure and content
        with tb.open_file(h5_path, mode='r') as h5:
            self.assertTrue('/datasets' in h5)
            self.assertTrue('/datasets/eps' in h5)
            self.assertTrue('/datasets/eps/epsr' in h5)
            self.assertTrue('/datasets/eps/epsi' in h5)

            # Calculate expected number of patches (approximate due to NaN filtering)
            # For this test, let's just check if *some* arrays were created
            epsr_group = h5.root.datasets.eps.epsr
            epsi_group = h5.root.datasets.eps.epsi
            num_epsr_arrays = len(list(epsr_group._f_iter_nodes()))
            num_epsi_arrays = len(list(epsi_group._f_iter_nodes()))

            self.assertTrue(num_epsr_arrays > 0)
            self.assertEqual(num_epsr_arrays, num_epsi_arrays)

            # Check number of permutations
            ssts = np.arange(*self.sst_range)
            mvs = np.arange(*self.ssm_range)
            expected_permuts = len(ssts) * len(mvs)

            # Check the total number of arrays based on patches processed and permutations
            # Get number of patches actually processed from the HDF5 attribute
            num_patches_processed = h5.root._v_attrs.num_arrays_added
            self.assertTrue(num_patches_processed > 0) # Ensure at least one patch was processed
            self.assertEqual(num_epsr_arrays, num_patches_processed * expected_permuts)

            # Check shape and type of one array
            first_epsr_array = next(iter(epsr_group._f_iter_nodes()))
            self.assertEqual(first_epsr_array.shape, self.patch_size)
            self.assertEqual(first_epsr_array.dtype, np.float32)

            # Check the attribute storing the number of processed patches
            self.assertTrue('num_arrays_added' in h5.root._v_attrs)
            # The number added should be <= dataset_size requested
            self.assertTrue(h5.root._v_attrs.num_arrays_added <= self.dataset_size)


    @patch('src.pysds.core.TDMRSDM')
    def test_run_resumes_simulation(self, mock_tdmrsdm_class):
        """Test if _run resumes simulation correctly based on HDF5 attribute."""
        # --- First run: Simulate a small number of patches ---
        initial_patches_to_simulate = 1
        mock_mrsdm_instance = MagicMock()
        dummy_eps_output = np.ones(self.patch_size, dtype=np.complex64) * (10 + 5j)
        mock_mrsdm_instance.run.return_value = dummy_eps_output
        mock_tdmrsdm_class.return_value = mock_mrsdm_instance

        # Run simulation with dataset_size = initial_patches_to_simulate
        sim1 = Simulator(
            workspace=os.path.join(self.base_workspace, self.workspace_name),
            dataset_size=initial_patches_to_simulate,
            patch_size=self.patch_size,
            soc_path=self.soc_path,
            freq_GHz=self.freq_GHz,
            sst_range=self.sst_range,
            ssm_range=self.ssm_range,
            no_data_limit=self.no_data_limit,
            logger=self.logger
        )

        # Define expected HDF5 file path
        sst_range_str = '_'.join(map(str, self.sst_range))
        ssm_range_str = '_'.join(map(str, self.ssm_range))
        h5_name = f'SDC_DP_DB_{self.workspace_name}_n{initial_patches_to_simulate}_{self.patch_size[0]}_FGHz{self.freq_GHz}_SST{sst_range_str}_SSM{ssm_range_str}.h5'
        h5_path = os.path.join(self.full_workspace_path, h5_name)

        # Check the attribute value after the first run
        with tb.open_file(h5_path, mode='r') as h5:
            self.assertEqual(h5.root._v_attrs.num_arrays_added, initial_patches_to_simulate)
            num_arrays_after_run1 = len(list(h5.root.datasets.eps.epsr._f_iter_nodes()))

        # --- Second run: Request more patches ---
        total_patches_to_simulate = 2 # Must be > initial_patches_to_simulate
        # Re-instantiate Simulator with the *same* parameters but larger dataset_size
        # It should detect the existing file and resume
        sim2 = Simulator(
            workspace=os.path.join(self.base_workspace, self.workspace_name),
            dataset_size=total_patches_to_simulate, # Request more now
            patch_size=self.patch_size,
            soc_path=self.soc_path,
            freq_GHz=self.freq_GHz,
            sst_range=self.sst_range,
            ssm_range=self.ssm_range,
            no_data_limit=self.no_data_limit,
            logger=self.logger
        )

        # Check the attribute value and number of arrays after the second run
        # Note: The filename is based on the *initial* dataset_size requested in the first run's __init__
        # This might be slightly confusing behavior, but we test based on how the code is written.
        # If the intention is to use the *new* dataset_size in the filename on resume, the code needs adjustment.
        with tb.open_file(h5_path, mode='r') as h5:
             # The attribute should now reflect the total number simulated
            self.assertEqual(h5.root._v_attrs.num_arrays_added, total_patches_to_simulate)
            num_arrays_after_run2 = len(list(h5.root.datasets.eps.epsr._f_iter_nodes()))
            # Check that more arrays were added
            self.assertTrue(num_arrays_after_run2 > num_arrays_after_run1)
            # Check the total number of arrays corresponds to the final count
            ssts = np.arange(*self.sst_range)
            mvs = np.arange(*self.ssm_range)
            expected_permuts = len(ssts) * len(mvs)
            self.assertEqual(num_arrays_after_run2, total_patches_to_simulate * expected_permuts)


if __name__ == '__main__':
    unittest.main()
