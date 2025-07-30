"""see documentation @ ../../docs/topodefect.md"""

import numpy as np

from typing import Optional
from numpy import typing as npt

from PyMatterSim.reader.reader_utils import Snapshots
from PyMatterSim.writer.lammps_writer import write_dump_header
from PyMatterSim.utils.coarse_graining import gaussian_blurring


class TopoDefect:
    """
    Characterize topological defects from a vector field, it can be
    vibration mode, active matter flow, non-affine displacement field etc.
    """
    def __init__(
        self,
        snapshots: Snapshots,
        read_mode: Snapshots,
    ) -> None:
        """
        initialization to calculate the topological defect

        Input Args:
            snapshots (Snapshots): (reader.reader_utils.Snapshots): 
                         snapshot object of input trajectory
                         (returned by reader.dump_reader.DumpReader)
            read_mode (Snapshots): (reader.reader_utils.Snapshots): 
                         snapshot object of input trajectory
                         (returned by reader.dump_reader.DumpReader)
        """
        self.snapshots = snapshots
        self.read_mode = read_mode

    def topo_defect_2d(
        self,
        kconfig: int = 0,
        ngrid: int = 100,
        gaussian_cut: float = 5.0,
        outputfile: Optional[str] = None,
    ) -> npt.NDArray:
        """
        Calculate 2D topological defects for the k-th snapshot

        Args:
            kconfig (int): the target configuration to characterize the topological
                           defect, default 0 for the first configuration.
            ngrid (int, optional): Number of neighbors. Default 100.
            gaussian_cut (float, optional): the longest distance to consider 
                                            the gaussian probability
                                            or the contribution from the simulation 
                                            particles. Default 5.0.
            outputfile (str, optional): output file. Default None.
        """

        grids_UV = self.read_mode.snapshots.snapshots[kconfig].positions
        ngrids = np.array([ngrid, ngrid])
        ppp = np.array([1, 1])

        gb_position, grids_UV_flat = gaussian_blurring(
            self.snapshots,
            grids_UV[np.newaxis, :, :],
            ngrids,
            1.0,
            ppp,
            gaussian_cut=gaussian_cut,
        )

        theta = (
            np.arctan2(grids_UV_flat[:, :, 0], grids_UV_flat[:, :, 1]).ravel().reshape(ngrid, ngrid)
        )
        grids_UV_grid = grids_UV_flat[0].reshape(ngrid, ngrid, 2)
        pos_grid = gb_position[0].reshape(ngrid, ngrid, 2)
        delta_pos_grid = np.abs(pos_grid[1, 1] - pos_grid[0, 0]) / 2

        # Calculate angle differences for four edges (clockwise direction)
        # θ(x,y) - θ(x+1,y)
        right_diff = theta - np.roll(theta, -1, axis=0)
        # θ(x+1,y) - θ(x+1,y+1)
        top_diff = np.roll(theta, -1, axis=0) - np.roll(theta, (-1, -1), axis=(0, 1))
        # θ(x+1,y+1) - θ(x,y+1)
        left_diff = np.roll(theta, (-1, -1), axis=(0, 1)) - np.roll(theta, -1, axis=1)
        # θ(x,y+1) - θ(x,y)
        bottom_diff = np.roll(theta, -1, axis=1) - theta

        # Combine and normalize angle differences
        angles_diff = np.stack([right_diff, top_diff, left_diff, bottom_diff])
        # Normalize to [-π, π]
        angles_diff = (angles_diff + np.pi) % (2 * np.pi) - np.pi

        # Calculate winding numbers
        winding_nums = np.round(angles_diff.sum(axis=0) / (2 * np.pi))

        # Generate defect points directly without full-grid intermediate array
        defect_mask = winding_nums != 0

        # Create compact defect array with shape (n_defects, 3) containing:
        # [x_position, y_position, winding_number] for each defect
        defect_points = np.column_stack(
            [
                # pos_grid[..., 0][defect_mask] + delta_pos_grid[0],  # x-coordinate with offset
                # pos_grid[..., 1][defect_mask] + delta_pos_grid[1],  # y-coordinate with offset
                winding_nums[defect_mask]  # winding number (±1)
            ]
        )

        defect_points = np.column_stack(
            [*(pos_grid[defect_mask] + delta_pos_grid).T, winding_nums[defect_mask]]
        )

        # Separate positive (+1) and negative (-1) defects:
        # Positive defects have winding number == 1
        pos_mask = defect_points[:, 2] == 1

        # Positive defect coordinates
        X_positive = defect_points[pos_mask, 0]  # x-coordinates of +1 defects
        Y_positive = defect_points[pos_mask, 1]  # y-coordinates of +1 defects

        # Negative defect coordinates
        X_negative = defect_points[~pos_mask, 0]  # x-coordinates of -1 defects
        Y_negative = defect_points[~pos_mask, 1]  # y-coordinates of -1 defects

        if outputfile:
            with open(outputfile, "w", encoding="utf-8") as f:
                header = write_dump_header(
                    self.snapshots.snapshots[kconfig].timestep,
                    ngrid * ngrid + len(defect_points),
                    self.snapshots.snapshots[kconfig].boxbounds,
                    addson="fx fy",
                )
                f.write(header)

                atom_id = 1
                # Output vector field data on grid points, type = 1
                for i in range(ngrid):
                    for j in range(ngrid):
                        x_coord = pos_grid[..., 0][i, j]
                        y_coord = pos_grid[..., 1][i, j]
                        fx = grids_UV_grid[..., 0][i, j]
                        fy = grids_UV_grid[..., 1][i, j]
                        f.write(f"{atom_id} 1 {x_coord:.6f} {y_coord:.6f} {fx} {fy}\n")
                        atom_id += 1

                # Output positive/negative vortex points,
                # type = 2 (red positive winding) or 3 (blue negative winding)
                for k in enumerate(X_positive):
                    x_coord = X_positive[k]
                    y_coord = Y_positive[k]
                    f.write(f"{atom_id} 2 {x_coord:.6f} {y_coord:.6f} 0 0\n")
                    atom_id += 1
                for k in enumerate(X_negative):
                    x_coord = X_negative[k]
                    y_coord = Y_negative[k]
                    f.write(f"{atom_id} 3 {x_coord:.6f} {y_coord:.6f} 0 0\n")
                    atom_id += 1
                f.close()
        return grids_UV_grid
