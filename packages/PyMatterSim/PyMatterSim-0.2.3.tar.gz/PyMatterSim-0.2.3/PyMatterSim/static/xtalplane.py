"""
This module is used to analyze the crystal plane of the simulation box.
see documentation @ ../../docs/xtalplane.md

There are several steps:
(1) Get the quaternions of the particles
(2) Convert the quaternions to [hkl] directions
(3) Get the crystal plane of the particles and the density map
"""

from typing import Optional

import numpy as np
import numpy.typing as npt

from ovito.io import import_file
from ovito.modifiers import PolyhedralTemplateMatchingModifier

from scipy.spatial.transform import Rotation as scipy_rotation
from scipy.stats import gaussian_kde

from ..utils.logging import get_logger_handle

logger = get_logger_handle(__name__)

class OrientationAnalyzer:
    """
    This class is used to analyze the orientation of particles.
    """
    def __init__(
        self,
        dumpfile: str,
    ) -> None:
        """
        Initialize the orientation analyzer.

        Args:
            dumpfile: The name of the input snapshot file.
        
        Return:
            None
        """
        self.dumpfile = dumpfile
        logger.info(f"Start particle orientation analyzer for {dumpfile}")
    def get_quaternions_by_ovito(
        self,
        outputfile: Optional[str]=None
        ) -> npt.NDArray:
        """
        Extract quaternion orientations from simulation dump

        Args:
            outputfile: Optional prefix for saving hkls as .npy
        
        Returns:
            quaternions: The quaternions of the particles in numpy array
                shape: (nsnapshots, nparticles, 4)
        """
        logger.info("Reading data and extracting quaternions")

        # Build pipeline and attach PTM
        pipeline = import_file(self.dumpfile)
        ptm = PolyhedralTemplateMatchingModifier()
        ptm.output_orientation = True
        pipeline.modifiers.append(ptm)

        quaternions = []
        for nframe in range(pipeline.source.num_frames):
            logger.info(f"Processing frame {nframe}")
            data = pipeline.compute(nframe)
            orientations = np.array(data.particles['Orientation'])
            quaternions.append(orientations)

        quaternions = np.array(quaternions)

        if outputfile:
            logger.info(f"Saving quaternions to {outputfile}_quaternions.npy")
            np.save(f"{outputfile}_quaternions.npy", quaternions)

        return quaternions
    def get_xtal_plane_indices(
        self,
        quaternions: npt.NDArray,
        outputfile: Optional[str]=None
    ) -> tuple[npt.NDArray, npt.NDArray]:
        """
        Convert quaternions to [hkl] directions to get the crystal plane indices

        Args:
            outputfile: The name of the output file. (default: None)
            If not provided, the hkls and zero indices will not be saved but only returned.

        Returns:
            hkls: The [hkl] directions of the particles in numpy array
                shape: (nsnapshots, nparticles, 3) 
            zero_indices: The indices of the particles that are zero in numpy array
                shape: (nsnapshots, nparticles)
        """
        logger.info("Converting quaternions to [hkl] directions")
        hkls = []
        zero_indices = []
        for n in range(quaternions.shape[0]):
            quaternions_n = quaternions[n]
            zero_mask = np.all(quaternions_n==0, axis=1)

            # Replace zero quaternions with identity rotation
            quaternions_n[zero_mask] = np.array([0, 0, 0, 1])

            rot_matrix = scipy_rotation.from_quat(quaternions_n).as_matrix()
            z_axis = np.array([0, 0, 1])
            hkls_n = rot_matrix.transpose(0, 2, 1) @ z_axis
            hkls.append(hkls_n)
            zero_indices.append(zero_mask.astype(np.int32))

        hkls = np.array(hkls)
        zero_indices = np.array(zero_indices)

        if outputfile:
            logger.info(f"Saving [hkl] directions to {outputfile}_hkls.npy")
            np.save(f"{outputfile}_hkls.npy", hkls)
            logger.info(f"Saving zero indices to {outputfile}_zero_indices.npy")
            np.save(f"{outputfile}_zero_indices.npy", zero_indices)

        return hkls, zero_indices
    def run_hkls(self, outputfile: Optional[str]=None):
        """
        Run the orientation analyzer to get the [hkl] directions of the particles.
        This method is used to run the analyzer in a script.

        Args:
            outputfile: The name of the output file. (default: None)
            If not provided, the hkls and zero indices will not be saved but only returned.

        Returns:
            hkls: The [hkl] directions of the particles in numpy array
                shape: (nsnapshots, nparticles, 3) 
            zero_indices: The indices of the particles that are zero in numpy array
                shape: (nsnapshots, nparticles)
        """
        quaternions = self.get_quaternions_by_ovito(outputfile)
        hkls, zero_indices = self.get_xtal_plane_indices(quaternions, outputfile)
        return hkls, zero_indices

class StereographicProjection:
    """
    Calculate stereographic projection of multiple crystal planes [h,k,l] 
    (using (001) as projection plane)
    """
    def __init__(
        self,
        dumpfile: str,
        hkls: Optional[npt.NDArray] = None,
    ) -> None:
        """
        Initialize the stereographic projection.

        Args:
            dumpgfile: The name of the input snapshot file.
            hkls: The [hkl] directions of the particles in numpy array 
                shape: (nsnapshots, nparticles, 3) 
        Return:
            None
        """
        self.dumpfile = dumpfile
        if hkls is None:
            logger.info(f"Get hkls from {self.dumpfile} by using the OrientationAnalyzer class")
            self.hkls, _ = self.get_hkls()
        else:
            self.hkls = hkls 
    def get_hkls(self, outputfile: Optional[str]=None) -> npt.NDArray:
        """
        Get the [hkl] directions of the particles from the dump file
        by calling the OrientationAnalyzer class

        Args:
            outputfile: The name of the output file to save particle quarterions
            and hkls, associated with the zero indces. (default: None)

        Returns:
            hkls: The [hkl] directions of the particles in numpy array
                shape: (nsnapshots, nparticles, 3)
        """
        logger.info(f"Getting [hkl] directions from {self.dumpfile} by OrientationAnalyzer()")
        hkls, zero_indices = OrientationAnalyzer(self.dumpfile).run_hkls(outputfile=outputfile)
        if hkls.ndim == 2:
            hkls = hkls[np.newaxis, :, :]
            logger.info("Processing hkl directions of a single snapshot")
        return hkls, zero_indices
    def get_stereographic_projection(
        self,
        outputfile: Optional[str]=None
    ) -> tuple[npt.NDArray, npt.NDArray]:
        """
        Get the stereographic projection in cartesian and polar coordinates of the particles
        based on the [hkl] directions.

        Args:
            outputfile: The name of the output file. (default: None)

        Returns:
            polar: The stereographic projection in polar coordinates of particles in numpy array
                shape: (nsnapshots, nparticles, 2)
            cartesian: The stereographic projection in cartesian coordinates of particles 
                in numpy array shape: (nsnapshots, nparticles, 2)
        """
        polar = []
        cartesian = []
        for n in range(self.hkls.shape[0]):
            hkl_n = self.hkls[n]
            norms = np.linalg.norm(hkl_n, axis=1, ord=2)
            theta = np.arccos(hkl_n[:, 2] / norms)
            phi = np.arctan2(hkl_n[:, 1], hkl_n[:, 0])
            r = np.tan(theta / 2)
            polar.append(np.column_stack((phi, r)))
            cartesian.append(np.column_stack((r * np.cos(phi), r * np.sin(phi))))

        polar = np.array(polar)
        cartesian = np.array(cartesian)
        if outputfile:
            logger.info(f"Saving polar coordinates to {outputfile}_polar.npy")
            np.save(f"{outputfile}_polar.npy", polar)
            logger.info(f"Saving cartesian coordinates to {outputfile}_cartesian.npy")
            np.save(f"{outputfile}_cartesian.npy", cartesian)

        return cartesian, polar
    def __find_min_total_distance_vectorized(
        self,
        projections: npt.NDArray,
        targets: npt.NDArray
    ) -> int:
        """
        Find the minimum total distance between projections and targets.

        Args:
            projections: The projections in numpy array
                shape: (24, 2)
            targets: The targets in numpy array
                shape: (npoints, 2)

        Returns:
            min_idx: The index of the target with the minimum total distance
        """
        diff = projections[:, np.newaxis, :] - targets[np.newaxis, :, :]
        distances = np.linalg.norm(diff, axis=2)
        total_distances = distances.sum(axis=1)
        min_idx = np.argmin(total_distances)
        return min_idx
    def reduce_fundamental_zone(
        self,
        outputfile: Optional[str]=None
    ) -> npt.NDArray:
        """
        Reduce the hkls to the fundamental zone.

        Args:
            outputfile: The name of the output file. (default: None)

        Returns:
            reduced_hkls: The reduced hkls in numpy array
                shape: (nsnapshots, nparticles, 3)
        """
        o_group = scipy_rotation.create_group('O').as_matrix()
        inversion = -np.eye(3)
        symmetry_ops = np.vstack([o_group, o_group @ inversion])

        reference_points = np.array([
            [0., 0.],
            [0.30515865, 0.30515865],
            [0.41421356, 0.],
        ])

        reduced_hkls = []
        for n in range(self.hkls.shape[0]):
            reduced_hkls_n = []
            for i in range(self.hkls.shape[1]):
                all_equiv_rots = np.array([s @ self.hkls[n, i] for s in symmetry_ops])
                norms = np.linalg.norm(all_equiv_rots, axis=1, ord=2)
                theta = np.arccos(all_equiv_rots[:, 2] / norms)
                phi = np.arctan2(all_equiv_rots[:, 1], all_equiv_rots[:, 0])
                r = np.tan(theta / 2)
                cartesian = np.column_stack((r * np.cos(phi), r * np.sin(phi)))
                min_idx = self.__find_min_total_distance_vectorized(
               cartesian, reference_points
            )
                reduced_hkls_n.append(all_equiv_rots[min_idx])
            reduced_hkls.append(reduced_hkls_n)
        reduced_hkls = np.array(reduced_hkls)

        if outputfile:
            logger.info(f"Saving reduced hkls to {outputfile}_reduced_hkls.npy")
            np.save(f"{outputfile}_reduced_hkls.npy", reduced_hkls)
        return reduced_hkls
    def hkls_density(
        self,
        mask: Optional[npt.NDArray]=None,
        outputfile: Optional[str]=None
    ) -> tuple[npt.NDArray, npt.NDArray]:
        """
        Calculate density of stereographic projections for hkl directions.
       
        Inputs:
            mask: Optional mask to select hkls
                shape: (nsnapshots, nparticles)
                default: all noes
            outputfile: Optional path prefix to save density results 
            (saved as {outputfile}_density_hkls.npy)

        Returns:
            projection_density: normalized density with values in [0, 1]
                shape: (nsnapshots, nparticles)
        """
        if mask is None:
            mask = np.ones(self.hkls.shape[:2], dtype=bool)

        cartesian, _ = self.get_stereographic_projection(outputfile=outputfile)
        logger.info(f"The shape of the cartesian coordinates: {cartesian.shape}")

        projection_density = np.zeros(mask.shape, dtype=float)
        for n in range(cartesian.shape[0]):
            points_projection = cartesian[n][mask[n]]
            x = points_projection[:, 0]
            y = points_projection[:, 1]

            xy = np.vstack([x, y])
            z = gaussian_kde(xy)(xy)
            z = (z - z.min()) / (z.max() - z.min())

            # assign densities back to the correct positions
            projection_density[n][mask[n]] = z

        if outputfile:
            logger.info(f"Saving hkls density to {outputfile}_density_hkls.npy")
            np.save(f"{outputfile}_density_hkls.npy", projection_density)
        return projection_density, cartesian
