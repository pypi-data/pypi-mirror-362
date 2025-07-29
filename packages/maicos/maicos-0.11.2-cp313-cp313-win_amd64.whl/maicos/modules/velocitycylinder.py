#!/usr/bin/env python
#
# Copyright (c) 2025 Authors and contributors
# (see the AUTHORS.rst file for the full list of names)
#
# Released under the GNU Public Licence, v3 or any higher version
# SPDX-License-Identifier: GPL-3.0-or-later
"""Module for computing cylindrical velocity profiles."""

import logging

import MDAnalysis as mda

from ..core import ProfileCylinderBase
from ..lib.util import render_docs
from ..lib.weights import velocity_weights


@render_docs
class VelocityCylinder(ProfileCylinderBase):
    r"""Cartesian velocity profile across a cylinder.

    Reads in coordinates and velocities from a trajectory and calculates a velocity
    :math:`[\mathrm{Å/ps}]` or a flux per unit area :math:`[\mathrm{Å^{-2}\,ps^{-1}}]`
    profile along a given axis.

    The ``grouping`` keyword gives you fine control over the velocity profile, e.g. you
    can choose atomar or molecular velocities. Note that if the first one is employed
    for complex compounds, usually a contribution corresponding to the vorticity appears
    in the profile.

    ${CORRELATION_INFO_RADIAL}

    Parameters
    ----------
    ${PROFILE_CYLINDER_CLASS_PARAMETERS}
    ${VDIM_PARAMETER}
    ${FLUX_PARAMETER}

    Attributes
    ----------
    ${PROFILE_CYLINDER_CLASS_ATTRIBUTES}

    """

    def __init__(
        self,
        atomgroup: mda.AtomGroup,
        dim: int = 2,
        zmin: float | None = None,
        zmax: float | None = None,
        bin_width: int = 1,
        rmin: float = 0,
        rmax: float | None = None,
        refgroup: mda.AtomGroup | None = None,
        grouping: str = "atoms",
        unwrap: bool = True,
        pack: bool = True,
        bin_method: str = "com",
        output: str = "velocity.dat",
        concfreq: int = 0,
        jitter: float = 0.0,
        vdim: int = 0,
        flux: bool = False,
    ) -> None:
        self._locals = locals()
        if vdim not in [0, 1, 2]:
            raise ValueError("Velocity dimension can only be x=0, y=1 or z=2.")
        normalization = "volume" if flux else "number"

        super().__init__(
            atomgroup=atomgroup,
            unwrap=unwrap,
            pack=pack,
            jitter=jitter,
            concfreq=concfreq,
            dim=dim,
            zmin=zmin,
            zmax=zmax,
            bin_width=bin_width,
            rmin=rmin,
            rmax=rmax,
            refgroup=refgroup,
            grouping=grouping,
            bin_method=bin_method,
            output=output,
            weighting_function=velocity_weights,
            weighting_function_kwargs={"vdim": vdim},
            normalization=normalization,
        )

    def _prepare(self):
        logging.info("Analysis of the velocity profile.")
        super()._prepare()
