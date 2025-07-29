#!/usr/bin/env python
#
# Copyright (c) 2025 Authors and contributors
# (see the AUTHORS.rst file for the full list of names)
#
# Released under the GNU Public Licence, v3 or any higher version
# SPDX-License-Identifier: GPL-3.0-or-later
"""Base class for spherical analysis."""

import logging
from collections.abc import Callable

import MDAnalysis as mda
import numpy as np

from ..lib.math import transform_sphere
from ..lib.util import render_docs
from .base import ProfileBase
from .planar import AnalysisBase


@render_docs
class SphereBase(AnalysisBase):
    r"""Analysis class providing options and attributes for a spherical system.

    Provide the results attribute `r`.

    Parameters
    ----------
    ${ATOMGROUP_PARAMETER}
    ${SPHERE_CLASS_PARAMETERS}
    ${WRAP_COMPOUND_PARAMETER}

    Attributes
    ----------
    ${SPHERE_CLASS_ATTRIBUTES}
    pos_sph : numpy.ndarray
        positions in spherical coordinats (r, phi, theta)
    _obs.R : float
        Average length (in Å) along the radial dimension in the current frame.
    _obs.bin_pos : numpy.ndarray, (n_bins)
        Central bin position of each bin (in Å) in the current frame.
    _obs.bin_width : float
         Bin width (in Å) in the current frame
    _obs.bin_edges : numpy.ndarray, (n_bins + 1)
        Edges of the bins (in Å) in the current frame.
    _obs.bin_area : numpy.ndarray, (n_bins)
        Surface area (in Å^2) of the sphere of each bin with radius `bin_pos` in the
        current frame. Calculated via :math:`4 \pi r_i^2` where :math:`i` is the index
        of the bin.
    results.bin_volume : numpy.ndarray, (n_bins)
        volume of a spherical shell of each bins (in Å^3) of the current frame.
        Calculated via :math:`4\pi/3 \left(r_{i+1}^3 - r_i^3 \right)` where `i` is the
        index of the bin.

    """

    def __init__(
        self,
        atomgroup: mda.AtomGroup,
        unwrap: bool,
        pack: bool,
        refgroup: mda.AtomGroup | None,
        jitter: float,
        concfreq: int,
        rmin: float,
        rmax: None | float,
        bin_width: float,
        wrap_compound: str,
    ):
        super().__init__(
            atomgroup=atomgroup,
            unwrap=unwrap,
            pack=pack,
            refgroup=refgroup,
            jitter=jitter,
            concfreq=concfreq,
            wrap_compound=wrap_compound,
        )

        self.rmin = rmin
        self._rmax = rmax
        self._bin_width = bin_width

    def _compute_lab_frame_sphere(self):
        """Compute lab limit `rmax`."""
        box_half = self.box_lengths.min() / 2
        if self._rmax is None:
            self.rmax = box_half
        elif self._rmax <= box_half:
            self.rmax = self._rmax
        else:
            logging.warning(
                f"`rmax` is bigger than half the smallest box vector ({box_half:.2f}) "
                "in the radial direction. This will lead to artifacts at the edges."
            )
            self.rmax = self._rmax
        # enforce calculations in double precision
        self.rmin = np.float64(self.rmin)
        self.rmax = np.float64(self.rmax)
        # Transform into spherical coordinates
        self.pos_sph = transform_sphere(
            self._universe.atoms.positions, origin=self.box_center
        )

    def _prepare(self):
        """Prepare the spherical analysis."""
        self._compute_lab_frame_sphere()

        if self.rmin < 0:
            raise ValueError("Only values for `rmin` larger or equal 0 are allowed.")

        if self._rmax is not None and self._rmax <= self.rmin:
            raise ValueError("`rmax` can not be smaller than or equal to `rmin`!")

        try:
            if self._bin_width > 0:
                R = self.rmax - self.rmin
                self.n_bins = int(np.ceil(R / self._bin_width))
            else:
                raise ValueError("Binwidth must be a positive number.")
        except TypeError as err:
            raise ValueError("Binwidth must be a number.") from err

    def _single_frame(self):
        """Single frame for the sphercial analysis."""
        self._compute_lab_frame_sphere()
        self._obs.R = self.rmax - self.rmin

        self._obs.bin_edges = np.linspace(
            self.rmin, self.rmax, self.n_bins + 1, endpoint=True
        )

        self._obs.bin_width = self._obs.R / self.n_bins
        self._obs.bin_pos = self._obs.bin_edges[1:] - self._obs.bin_width / 2
        self._obs.bin_area = 4 * np.pi * self._obs.bin_pos**2
        self._obs.bin_volume = 4 * np.pi * np.diff(self._obs.bin_edges**3) / 3

    def _conclude(self):
        """Results calculations for the sphercial analysis."""
        super()._conclude()
        self.results.bin_pos = self.means.bin_pos


@render_docs
class ProfileSphereBase(SphereBase, ProfileBase):
    """Base class for computing radial profiles in a spherical geometry.

    ${CORRELATION_INFO_RADIAL}

    Parameters
    ----------
    ${PROFILE_SPHERE_CLASS_PARAMETERS}
    ${PROFILE_CLASS_PARAMETERS_PRIVATE}

    Attributes
    ----------
    ${PROFILE_CYLINDER_CLASS_ATTRIBUTES}

    """

    def __init__(
        self,
        atomgroup: mda.AtomGroup,
        unwrap: bool,
        pack: bool,
        refgroup: mda.AtomGroup | None,
        jitter: float,
        concfreq: int,
        rmin: float,
        rmax: None | float,
        bin_width: float,
        grouping: str,
        bin_method: str,
        output: str,
        weighting_function: Callable,
        weighting_function_kwargs: dict | None,
        normalization: str,
    ):
        SphereBase.__init__(
            self,
            atomgroup=atomgroup,
            unwrap=unwrap,
            pack=pack,
            refgroup=refgroup,
            jitter=jitter,
            concfreq=concfreq,
            rmin=rmin,
            rmax=rmax,
            bin_width=bin_width,
            wrap_compound=grouping,  # same as grouping to avoid broken compounds
        )
        # `AnalysisBase` performs conversions on `atomgroup`.
        # Take converted `atomgroup` and not the user provided ones.
        ProfileBase.__init__(
            self,
            atomgroup=self.atomgroup,
            grouping=grouping,
            bin_method=bin_method,
            output=output,
            weighting_function=weighting_function,
            weighting_function_kwargs=weighting_function_kwargs,
            normalization=normalization,
        )

    def _prepare(self):
        SphereBase._prepare(self)
        ProfileBase._prepare(self)

        logging.info(
            """Profile along the radial coordinate in a spherical """
            """coordinate system."""
        )

    def _compute_histogram(
        self, positions: np.ndarray, weights: np.ndarray | None = None
    ) -> np.ndarray:
        positions = transform_sphere(positions, origin=self.box_center)[:, 0]
        hist, _ = np.histogram(
            positions, bins=self.n_bins, range=(self.rmin, self.rmax), weights=weights
        )

        return hist

    def _single_frame(self) -> float:
        SphereBase._single_frame(self)
        ProfileBase._single_frame(self)

        # Take the center bin of the zeroth group for correlation analysis.
        return self._obs.profile[0]

    def _conclude(self):
        SphereBase._conclude(self)
        ProfileBase._conclude(self)
