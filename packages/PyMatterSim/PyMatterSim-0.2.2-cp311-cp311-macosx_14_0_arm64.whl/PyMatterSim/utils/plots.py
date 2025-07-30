"""
add plot functions for different pruposes:

1. plot the stereographic projection of the crystal plane
"""

from typing import Optional, Literal

import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt

from scipy.interpolate import griddata
from matplotlib.path import Path
from matplotlib.patches import Polygon
from ..utils.logging import get_logger_handle

logger = get_logger_handle(__name__)
def plot_stereographic_projection(
    outputfile: str,
    cartesian: Optional[npt.NDArray] = None,
    values: Optional[npt.NDArray] = None,
    points_show: Optional[npt.NDArray] = None,
    color_range: Literal["full_range", "min_max"] = "min_max"
):
    """
    Plot stereographic projection with color-mapped values.

    Parameters:
        outputfile: Optional path to save figure.
        cartesian: Cartesian coordinates (on stereographic plane)
            shape: (nparticles, 2)
        values: Value array (e.g., density/energy)
            shape: (nparticles,)
        points_show: Specific HKLs to mark (3D vectors, shown as dots on projection)
            shape: (n_show, 3)
        color_range: 'full_range' for [0,1], 'min_max' for data min/max scaling.
    """

    logger.info("Plot stereographic projection of xtal plane and save to pdf file")
    cartesian = np.array(cartesian)
    values = np.array(values)
    points_show = np.array(points_show)

    # Define triangle vertices and crystal plane label data
    triangle_vertices = np.array([
        [0.,         0.        ],
        [0.07071421, 0.07071421],
        [0.1583124,  0.1583124 ],
        [0.22474487, 0.22474487],
        [0.30515865, 0.30515865],
        [0.3660254,  0.3660254 ],
        [0.38449988, 0.28837491],
        [0.4,        0.2       ],
        [0.41048533, 0.10262133],
        [0.41421356, 0.        ],
        [0.33333333, 0.        ],
        [0.23606798, 0.        ],
        [0.09901951, 0.        ]
    ])

    _, ax = plt.subplots(figsize=(8, 8))

    if cartesian.any() and values.any() == None:
        ax.scatter(
            cartesian[:, 0], cartesian[:, 1],
            s=1, alpha=0.1, color='black', 
            edgecolor='white', linewidth=1
        )

    if cartesian.any() and values.any():
        # Create grid for interpolation
        xi = np.linspace(
            triangle_vertices[:, 0].min(),
            triangle_vertices[:, 0].max(),
            300
        )
        yi = np.linspace(
            triangle_vertices[:, 1].min(),
            triangle_vertices[:, 1].max(),
            300
        )
        xi, yi = np.meshgrid(xi, yi)
        zi = griddata(cartesian, values, (xi, yi), method='cubic', fill_value=0)

        polygon = Path(triangle_vertices)
        points = np.vstack((xi.flatten(), yi.flatten())).T
        mask = polygon.contains_points(points).reshape(xi.shape)
        zi_masked = np.where(mask, zi, np.nan)

        if color_range == "full_range":
            vmin, vmax = 0.0, 1.0
        elif color_range == "min_max":
            vmin, vmax = values.min(), values.max()
            
        im = ax.pcolormesh(xi, yi, zi_masked, shading='auto', cmap='rainbow', vmin=vmin, vmax=vmax)
        plt.colorbar(im, ax=ax, shrink=0.5)

    # Draw triangular region boundary
    ax.add_patch(Polygon(triangle_vertices, edgecolor='black', facecolor='none', linewidth=1.5))
    # Define crystal plane label data
    label_data = [
        # (hkl, position, text_offset, rotation)
        ([1,1,7], [0.07071421, 0.07071421], [-0.01, 0.01], 45),
        ([1,1,3], [0.1583124, 0.1583124], [-0.01, 0.01], 45),
        ([1,1,2], [0.22474487, 0.22474487], [-0.01, 0.01], 45),
        ([3,3,4], [0.30515865, 0.30515865], [-0.01, 0.01], 45),
        ([4,3,4], [0.38449988, 0.28837491], [0.015, 0.004], -73),
        ([2,1,2], [0.4, 0.2], [0.015, 0.002], -80),
        ([4,1,4], [0.41048533, 0.10262133], [0.015, 0], -85),
        ([1,0,5], [0.09901951, 0], [0, -0.015], 0),
        ([3,0,4], [0.33333333, 0], [0, -0.015], 0),
        ([1,0,2], [0.23606798, 0], [0, -0.015], 0)]
    # Draw crystal plane labels
    for hkl, (x, y), (dx, dy), rot in label_data:
        label = f"({hkl[0]}{hkl[1]}{hkl[2]})"
        ax.scatter(x, y, s=40, color='black', edgecolor='white', linewidth=1)
        ax.text(x+dx, y+dy, label, fontsize=9, ha='center', va='center', rotation=rot)
    # Label triangle vertices
    vertex_labels = [
        ((0, 0), "(001)", (-0.04, -0.01), 'bottom'),
        ((0.4142, 0), "(101)", (0.04, -0.01), 'bottom'),
        ((0.3660, 0.3660), "(111)", (0, 0.01), 'bottom')
    ]

    for (vx, vy), lbl, (dx, dy), va in vertex_labels:
        ax.text(vx + dx, vy + dy, lbl, fontsize=15, ha='center', va=va)

    # Draw the special points
    if points_show.any():
        points_show = np.array(points_show)
        norms = np.linalg.norm(points_show, axis=1, ord=2)
        theta = np.arccos(points_show[:, 2] / norms)
        phi = np.arctan2(points_show[:, 1], points_show[:, 0])
        r = np.tan(theta / 2)
        points_projection = np.column_stack((r * np.cos(phi), r * np.sin(phi)))

        for hkl, (x, y) in zip(points_show, points_projection):
            label = f"$\\overline{{{abs(hkl[0])}}}$" if hkl[0] < 0 else str(hkl[0])
            label += f"$\\overline{{{abs(hkl[1])}}}$" if hkl[1] < 0 else str(hkl[1])
            label += f"$\\overline{{{abs(hkl[2])}}}$" if hkl[2] < 0 else str(hkl[2])
            label = f"({label})"

            ax.scatter(x, y, s=40, color='black', edgecolor='white', linewidth=1, zorder=10)
            ax.text(x, y+0.015, label, fontsize=9, ha='center', va='center', zorder=5)

    # Chart properties
    ax.set_xlim(-0.05, 0.5)
    ax.set_ylim(-0.05, 0.4)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.grid(False)
    plt.tight_layout()
    plt.savefig(f'{outputfile}_stereoproj.pdf', dpi=600)
    plt.close()