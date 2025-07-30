"""Test suite for OrientationAnalyzer and StereographicProjection in PyMatterSim"""

import os
import unittest
import numpy as np

from PyMatterSim.utils.logging import get_logger_handle
from PyMatterSim.static.xtalplane import OrientationAnalyzer, StereographicProjection

logger = get_logger_handle(__name__)

READ_TEST_FILE_PATH = "tests/sample_test_data"

class TestOrientationAnalyzer(unittest.TestCase):
    """
    Test class for OrientationAnalyzer
    """
    def setUp(self) -> None:
        super().setUp()
        self.test_file = f"{READ_TEST_FILE_PATH}/xtalplane.dump"
        self.output_prefix = "test_orientation"
        self.cleanup_files = [
            f"{self.output_prefix}_quaternions.npy",
            f"{self.output_prefix}_hkls.npy",
            f"{self.output_prefix}_zero_indices.npy"
        ]

    def tearDown(self) -> None:
        for f in self.cleanup_files:
            if os.path.exists(f):
                os.remove(f)

    def test_get_quaternions_by_ovito(self):
        """
        Test get_quaternions_by_ovito returns correct shape and saves file
        """
        analyzer = OrientationAnalyzer(self.test_file)
        quaternions = analyzer.get_quaternions_by_ovito(outputfile=self.output_prefix)

        # Check returned array shape
        self.assertEqual(quaternions.ndim, 3)  # (nsnapshots, nparticles, 4)

        # Check file was saved
        self.assertTrue(os.path.exists(f"{self.output_prefix}_quaternions.npy"))
        self.tearDown()

    def test_get_xtal_plane_indices(self):
        """
        Test get_xtal_plane_indices with dummy numpy quaternions
        """
        analyzer = OrientationAnalyzer("dummy.dump")

        # Dummy data: (1 snapshot, 3 particles, 4 components)
        quaternions = np.array([
            [
                [0, 0, 0, 1],
                [0, 0, 0, 0],
                [0.707, 0, 0, 0.707]
            ]
        ])

        hkls, zero_indices = analyzer.get_xtal_plane_indices(
            quaternions, outputfile=self.output_prefix
        )

        # Check shapes
        self.assertEqual(hkls.shape, (1, 3, 3))
        self.assertEqual(zero_indices.shape, (1, 3))

        # Check zero detection
        np.testing.assert_array_equal(zero_indices, np.array([[0, 1, 0]]))

        # Check file was saved
        self.assertTrue(os.path.exists(f"{self.output_prefix}_hkls.npy"))
        self.assertTrue(os.path.exists(f"{self.output_prefix}_zero_indices.npy"))
        self.tearDown()

    def test_run_hkls(self):
        """
        Test run_hkls end-to-end
        """
        analyzer = OrientationAnalyzer(self.test_file)
        hkls, zero_indices = analyzer.run_hkls(outputfile=self.output_prefix)

        # Check returned shapes
        self.assertEqual(hkls.ndim, 3)
        self.assertEqual(zero_indices.ndim, 2)

        # Check files were saved
        for f in self.cleanup_files:
            self.assertTrue(os.path.exists(f))
        self.tearDown()

class TestStereographicProjection(unittest.TestCase):
    """
    Tests for StereographicProjection class
    """
    def setUp(self) -> None:
        self.test_file = f"{READ_TEST_FILE_PATH}/xtalplane.dump"
        self.output_prefix = "test_stereo"
        self.cleanup_files = [
            f"{self.output_prefix}_quaternions.npy",
            f"{self.output_prefix}_hkls.npy",
            f"{self.output_prefix}_zero_indices.npy",
            f"{self.output_prefix}_polar.npy",
            f"{self.output_prefix}_cartesian.npy",
            f"{self.output_prefix}_reduced_hkls.npy",
            f"{self.output_prefix}_density_hkls.npy"
        ]
        self.proj = StereographicProjection(self.test_file)
        self.tearDown()

    def tearDown(self) -> None:
        for f in self.cleanup_files:
            if os.path.exists(f):
                os.remove(f)

    def test_get_hkls(self):
        """
        Test get_hkls returns correct shape and can save file
        """
        hkls = self.proj.get_hkls(outputfile=self.output_prefix)[0]
        self.assertEqual(hkls.ndim, 3)  # (nsnapshots, nparticles, 3)
        self.tearDown()

    def test_get_stereographic_projection(self):
        """
        Test get_stereographic_projection with dummy hkls
        """
        hkls = np.array([[
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 1]
        ]])
        
        proj = StereographicProjection(self.test_file, hkls)
        
        cartesian, polar = proj.get_stereographic_projection(
            outputfile=self.output_prefix
        )

        self.assertEqual(cartesian.shape, (1, 4, 2))
        self.assertEqual(polar.shape, (1, 4, 2))
        self.assertTrue(os.path.exists(f"{self.output_prefix}_polar.npy"))
        self.assertTrue(os.path.exists(f"{self.output_prefix}_cartesian.npy"))
        self.tearDown()
    def test_reduce_fundamental_zone(self):
        """
        Test reduce_fundamental_zone
        """
        reduced_hkls = self.proj.reduce_fundamental_zone(outputfile=self.output_prefix)
        self.assertEqual(reduced_hkls.shape, self.proj.hkls.shape)
        self.assertTrue(os.path.exists(f"{self.output_prefix}_reduced_hkls.npy"))
        self.tearDown()
    def test_hkls_density(self):
        """
        Test hkls_density
        """
        density, cartesian = self.proj.hkls_density(outputfile=self.output_prefix)

        self.assertEqual(density.shape, self.proj.hkls.shape[:2])
        self.assertEqual(cartesian.shape[:2], self.proj.hkls.shape[:2])
        self.assertTrue(os.path.exists(f"{self.output_prefix}_density_hkls.npy"))
        self.tearDown()