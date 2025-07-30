<!--
Copyright (C) 2024- Davide Mollica <davide.mollica@inaf.it>
SPDX-License-Identifier: GPL-3.0-or-later

This file is part of iactsim.

iactsim is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

iactsim is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with iactsim.  If not, see <https://www.gnu.org/licenses/>.
-->

# iactsim: Imaging Atmospheric Cherenkov Telescope Simulation

[![License](https://img.shields.io/badge/license-GPLv3-blue)](LICENSE) 
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/downloads/) 
[![Build Status](https://gitlab.com/davide.mollica/iactsim/badges/dev/pipeline.svg)](https://gitlab.com/davide.mollica/iactsim/-/pipelines)
<!-- [![Release](https://gitlab.com/davide.mollica/iactsim/-/badges/CI/release.svg)](https://gitlab.com/davide.mollica/iactsim/-/releases) -->

<!-- [![DOI](https://zenodo.org/badge/DOI/YOUR_DOI_HERE.svg)](https://doi.org/YOUR_DOI_HERE) -->
<!-- [![PyPI version](https://badge.fury.io/py/iact-sim.svg)](https://badge.fury.io/py/iact-sim)  -->
## Overview

`iactsim` is a Python package designed for simulating the response of Imaging Atmospheric Cherenkov Telescopes (IACTs). It exploits the computational power of GPUs to accelerate computationally intensive tasks such as ray-tracing and SiPM response simulation. This project aims to provide a fast, flexible, and user-friendly simulation framework for IACT performance studies, instrument design and data analysis.

- [**Software documentation**](https://iact-sim-49dba6.gitlab.io/)
- [**Source code**](https://gitlab.com/davide.mollica/iactsim)

## Features
*   GPU-accelerated ray-tracing
*   GPU-accelerated camera response
*   Runtime configuration
*   And more...

## Installation

### Prerequisites

*   **Python**: >=3.12

*   **NVIDIA HPC SDK**: `iactsim` requires the NVIDIA HPC Software Development Kit (SDK) to compile CUDA kernels

*   **CuPy**: `iactsim` utilizes CuPy for GPU offloading

*   **CMake**: >=3.15

*   **A C++ compiler**: ``gcc`` or ``nvcc``

### Installation Instructions
It is **recommended** to use a virtual environment. For example, using `mamba`:
```bash
mamba create -n simenv python=3.13
mamba activate simenv
```

You need a compiler for the C++ part. If you use HPC SDK compilers, as recommended here, you can use them
with `module load nvhpc` before calling `pip`. You can choose ``gcc`` or ``nvcc`` appending ``-C cmake.args="-DCMAKE_CXX_COMPILER=<compiler_name>"`` to the install command, replacing ``<compiler_name>`` with the actual compiler name.

#### **(PyPI)**
`iactsim` source archive is available on `PyPI`:
```bash
pip install iactsim -v
```

#### **(dev)**
- Clone the repository:
    
    ```bash
    git clone https://gitlab.com/davide.mollica/iactsim.git
    ```

- Move inside the cloned folder and install `iactsim` from source:
    
    ```bash    
    cd iactsim
    python -m pip install . -v
    ```

#### zlib
For the C++ part, by deafult [``zlib-ng``](https://github.com/zlib-ng/zlib-ng) (*zlib data compression library for the next generation systems*) will be used (cmake will clone the repo automatically). If you have to use [``zlib``](https://zlib.net/) or you do not need to decompress gzip CORSIKA files, you can append ``-C cmake.args="-DUSE_ZLIBNG=OFF"`` to the install command.

#### NVHPC
[Configure the enviroment](https://docs.nvidia.com/hpc-sdk//hpc-sdk-install-guide/index.html#install-linux-end-usr-env-settings) to use HPC SDK compilers (you can download HPC SDK from the [NVIDIA website](https://developer.nvidia.com/hpc-sdk)). We suggest to use [Environment Modules](https://modules.readthedocs.io/en/latest/) to handle SDK configuration and then define `NVCC` and `CUDA_PATH` enviromental variables:
```bash
module load nvhpc
export NVCC=$NVHPC_ROOT/compilers/bin/nvcc
export CUDA_PATH=$NVHPC_ROOT/cuda
```
With `conda`/`mamba` enviroments you can use the provided configuration script `configure_conda_env`
```bash
mamba activate simenv
configure_conda_env simenv
mamba deactivate
```
This adds an activation script and a deactivation script to the `simenv` enviroment that will automatically handle the configuration when it is activated or deactivated.

#### Install CuPy
```bash
pip install cupy-cuda<XXX>
```
Replace <XXX> with your CUDA version (e.g., `cupy-cuda12x`).
For more detailed instructions on installing CuPy, refer to the [CuPy documentation](https://docs.cupy.dev/en/stable/install.html).

#### Conda virtual environments and Jupyter
If you want to run Jupyter Notebook or JupyterLab from a different environment (usually the base environment) and access the new one, do the following:

  1.  Install [nb_conda_kernels](https://github.com/Anaconda-Platform/nb_conda_kernels) in the base environment:
        ```bash
        mamba deactivate
        mamba install nb_conda_kernels 
        ```

  2.  Make sure `ipykernel` is installed in the new virtual environment
        ```bash
        mamba install -n simenv ipykernel
        ```
Now you can find the new environment kernel in JupyterLab/Notebook kernels list (`Kernel->Change kernel` in the menu bar).

In order to let the `tqdm` progress bar work properly, install `ipywidgets` following the [installation guide](https://ipywidgets.readthedocs.io/en/stable/user_install.html).

## Usage

### Optical system definition
```python
import iactsim
import matplotlib.pyplot as plt

plt.style.use('iactsim.iactsim')

# Spherical mirror
mirror_curvature_radius = 20000
plate_scale = mirror_curvature_radius/57.296/2.
mirror = iactsim.optics.SphericalSurface(
    half_aperture=10000., 
    curvature=1./mirror_curvature_radius,
    position=(0,0,0),
    surface_type=iactsim.optics.SurfaceType.REFLECTIVE_OUT, # reflective in the pointing direction
    name = 'Mirror'
)

# Flat focal surface (5deg hexagon)
focal_plane = iactsim.optics.FlatSurface(
    half_aperture = 5*plate_scale, 
    position = (0,0,0.5*mirror_curvature_radius),
    aperture_shape = iactsim.optics.ApertureShape.HEXAGONAL,
    surface_type=iactsim.optics.SurfaceType.SENSITIVE_IN, # sensitive surface opposite to the pointing direction
    name = 'Focal Plane'
)

# Optical system
os = iactsim.optics.OpticalSystem(surfaces=[focal_plane, mirror], name='TEST-OS')

# Telescope position
pos = (0,0,0)

# Telescope pointing (alt,az)
poi = (0.,0.)

# IACT
telescope = iactsim.IACT(os, position=pos, pointing=poi)

# Copy data to the device
telescope.cuda_init()

# Photon source initialized on-axis 
source = iactsim.optics.sources.Source(telescope)
source.positions.radial_uniformity = False
source.positions.random = False

# Plot spot diagram at different off-axis angles
n_plots = 5
fig, axes = plt.subplots(1,n_plots,figsize=(3.5*n_plots,3.5))

source.directions.altitude -= 2.
for ax in axes:
    # Adjust photon position to match the mirror position
    source.set_target('Mirror')
    
    # Generate photons
    ps, vs, wls, ts = source.generate(10000)
    
    # Perform ray-tracing
    telescope.trace_photons(ps, vs, wls, ts)
    
    # Plot spot diagram
    iactsim.visualization.scatter(ps, s=0.2, ax=ax, color='black', alpha=0.5, scale=plate_scale)
    ax.set_xlabel('X (deg)')
    ax.set_ylabel('Y (deg)')
    ax.grid(ls='--')

    # Move the source
    source.directions.altitude += 1. # degree

plt.tight_layout()
plt.show()
```

<img src="https://gitlab.com/davide.mollica/iactsim/-/raw/dev/media/psf.png?ref_type=heads" alt="Alt text" width="100%">

### Mirror segmentation

The following code provides an example of how to segment a surface (`AsphericalSurface`, `SphericalSurface` or `FlatSurface`) starting from a mother surface (in this case `mirror`).
Note that each segment is an independent surface and does not need a mother surface, which is used here simply for convenience.

```python
import numpy as np

# List of segments
segments = []

# Segment ID
k = 0

# Segments on a 10X10 grid, 80 total
n = 10

segment_distance = 2*mirror.half_aperture / (n+3)

for i in range(n+3):
    for j in range(n+3):
        offset = [-mirror.half_aperture+segment_distance*i, -mirror.half_aperture+segment_distance*j]
        r_segment = np.sqrt(offset[0]**2+offset[1]**2)
        
        # Do not create segments outside the original mirror aperture
        if r_segment > mirror.half_aperture-segment_distance*np.sqrt(2):
            continue

        # Ideal segment position
        segment_position = [
            offset[0],
            offset[1],
            mirror.sagitta(r_segment),
        ]
        
        # Create the surface
        segment = iactsim.optics.SphericalSurface(
            curvature=mirror.curvature,
            half_aperture=0.45*segment_distance, 
            position=segment_position,
            surface_type=mirror.type,
            name = f'Segment-{k}',
            aperture_shape=iactsim.optics.ApertureShape.SQUARE,
            tilt_angles=np.random.normal(0,1,3), # Big random dispersion
            scattering_dispersion=0.05
        )
        
        # Specify the segment offset
        # When a segment is created in this way:
        #  - it will be oriented with the same surface normal 
        #    of the mother surface at the specified offset 
        #  - `tilt_angles` attribute will define a deviation from this orientation.
        segment.offset = offset
        
        segments.append(segment)
        k += 1

# Optical system
segmented_os = iactsim.optics.OpticalSystem(surfaces=[focal_plane, *segments], name='SEGMENTED-TEST-OS')

# IACT
segmented_telescope = iactsim.IACT(segmented_os, position=pos, pointing=poi)
segmented_telescope.cuda_init()

# Plot spot diagram at different off-axis angles
n_plots = 5
fig, axes = plt.subplots(1,n_plots,figsize=(3.5*n_plots,3.5))

# Photon source initialized on-axis 
source = iactsim.optics.sources.Source(segmented_telescope)
source.positions.radial_uniformity = False
source.positions.random = False
source.positions.r_max = mirror.half_aperture*1.5

source.directions.altitude -= 2.
for ax in axes:
    # Adjust photon position to match the mirror position
    source.set_target()
    
    # Generate photons
    ps, vs, wls, ts = source.generate(10000)
    
    # Perform ray-tracing
    segmented_telescope.trace_photons(ps, vs, wls, ts)
    
    # Plot spot diagram
    iactsim.visualization.scatter(ps, s=0.2, ax=ax, color='black', alpha=0.5, scale=plate_scale)
    ax.set_xlabel('X (deg)')
    ax.set_ylabel('Y (deg)')
    ax.grid(ls='--')

    # Move the source
    source.directions.altitude += 1. # degree

plt.tight_layout()
plt.show()
```

<img src="https://gitlab.com/davide.mollica/iactsim/-/raw/dev/media/segmented_psf.png?ref_type=heads" alt="Alt text" width="100%">

### Visualize your geometry

For optical systems with complex geometry, it is often useful to perform a visual check of the geometry. To do so, a [VTK](https://docs.vtk.org/en/latest/getting_started/index.html) visualizer is provided:
```python
renderer = iactsim.visualization.VTKOpticalSystem(segmented_telescope.optical_system)
renderer.start_render()
```

<div style="text-align: center;">
    <img src="https://gitlab.com/davide.mollica/iactsim/-/raw/dev/media/vtk_os.png?ref_type=heads" alt="Alt text" width="35%">
</div>
