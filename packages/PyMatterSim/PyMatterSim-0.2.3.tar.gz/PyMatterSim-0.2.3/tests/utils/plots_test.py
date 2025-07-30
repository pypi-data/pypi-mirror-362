"""Test suite for plotting stereographic projections in PyMatterSim"""

import os
import unittest
import numpy as np

from PyMatterSim.utils.logging import get_logger_handle
from PyMatterSim.utils.plots import plot_stereographic_projection

logger = get_logger_handle(__name__)

class TestPlotStereographicProjection(unittest.TestCase):
    """
    Test plot_stereographic_projection
    """
    def setUp(self) -> None:
        self.output_prefix = "test_stereo_plot"
        self.output_pdf = f"{self.output_prefix}_stereoproj.pdf"

    def tearDown(self) -> None:
        if os.path.exists(self.output_pdf):
            os.remove(self.output_pdf)
    def test_plot_stereographic_projection(self) -> None:
        """
        Test the stereographic projection plotting function.
        """
        logger.info("Testing stereographic projection plotting function")
        # dummy cartesian projection points
        cartesian = np.array([
            [0.1, 0.1],
            [0.2, 0.05],
            [0.3, 0.15],
            [0.2,0.25]
        ])
        # dummy values (normalized density, for example)
        values = np.array([0.3, 0.7, 0.9, 0.1])

        # dummy points_show (3D HKL vectors)
        points_show = np.array([
            [4, 3, 5],
            [2, 1, 3]
        ])

        plot_stereographic_projection(
            outputfile=self.output_prefix,
            cartesian=cartesian,
            values=values,
            points_show=points_show
            )

        self.assertTrue(os.path.exists(self.output_pdf), f"{self.output_pdf} not created")
        os.remove(self.output_pdf)
