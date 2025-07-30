# Ripple

[![PyPI version](https://badge.fury.io/py/Ripple.svg)](https://badge.fury.io/py/Ripple)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Ripple is a high-performance Python package for scalable analysis of particle‐motion correlation functions. Exploiting multicore parallelism on HPC systems, Ripple rapidly computes correlation metrics for exceptionally large trajectory datasets—such as those produced by machine‐learning force fields. Trajectories are read through ASE, guaranteeing broad compatibility with virtually any supported file format. Computations are dispatched across multiple CPUs, and the resulting correlation data are exported as HDF5 files to a user-specified directory for downstream processing.

---

## Functions

- Mean square displacement (MSD)
- Collective mean square displacement (cMSD)
- Displacement cross correlation function
- Haven ratio
- Time averaged radial distribution function (RDF)
- Time averaged static structure factor (SSF)
- Van Hove correlation function self & distinct part (VHF_s, VHF_d)
- Intermediate scattering function self part & total (ISF_s, ISF_tot)

---

## Installation

Install via pip:

```bash
pip install git+https://github.com/Frost-group/Ripple
```
---

## Usage Example

Here’s a simple case:

```python
import ripple
from ripple import correlation

if __name__ == '__main__':
    v=0
    N_frame = 4000
    save_dir = f'Ripple_VHF_d/'
    target_atoms1 = 'Li'
    target_atoms2 = 'Li'
    r_max = 12
    dr = 0.02
    timestep = 0.1
    N_workers = 64
    for t in [200,250,300,350,400,450,500,550,600,650,700]:
        for r in [0,42,123,161,1234]:
            trajectory = ase.io.read(f'diffusion_rand={r}/MaceMD_{t}K_{v}vacancies_trajactory.xyz', format='extxyz', index=f':{N_frame}')
            trajectory_tag = f'{v}v_{r}randn_{t}K'
            vhf_distinct_cal(trajectory, trajectory_tag, save_dir, target_atoms1, target_atoms2, r_max, dr, timestep, N_workers)
```

After calculation, you will obtain a HDF5 file for each trajectory.

```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
import h5py

v=0
randn = [0, 42, 123, 161, 1234]
t = 400 #temperature = [200,250,300,350,400,450,500,550,600,650,700]
target_atom1 = 'Li'
target_atom2 = 'Li'
G_d = np.empty(len(randn), dtype=object)
for r in range(len(randn)):
    file = h5py.File(f'Ripple_VHF_d/vhfd_{target_atom1}_{target_atom2}_{v}v_{randn[r]}randn_{t}K.hdf5', 'r')
    G_d[r] = np.array(file[f'vhfd_{target_atom1}_{target_atom2}'])
    N_frame = int(np.array(file['N_frame']))
    timestep = float(np.array(file['timestep']))
    r_max = float(np.array(file['r_max']))

file.close()
G_d = np.mean(G_d, axis=0) # take average on diff randon mumbers
font_path = fm.findfont(fm.FontProperties(family='Times New Roman'))
font = fm.FontProperties(fname=font_path, size=16)
fig = plt.figure("plot", figsize=(8, 6), dpi=100)
plt.subplots_adjust(top=0.95, bottom=0.105, left=0.11, right=0.98, hspace=0.05, wspace=0.05)
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 16
fig.tight_layout(pad=0.0)
ax = fig.add_subplot(111)
im = ax.imshow(G_d.T, vmin=0.0, vmax=2.0, origin='lower', cmap='coolwarm', extent=[0, N_frame*timestep, 0, r_max], aspect='auto')
ax.set_yticks(np.linspace(0, r_max, 5))
ax.set_xticks(np.linspace(0, N_frame*timestep, 5))
ax.tick_params(axis='both', which='both', direction='inout', length=5.0, width=2.0, color='black')
ax.set_ylabel('r (Å)', fontproperties=font)
ax.set_xlabel('t (ps)', fontproperties=font)
plt.colorbar(im)
fig.show()
```
![G_d_Li_Li_0v_400K](./images/G_d_Li_Li_0v_400K.png)