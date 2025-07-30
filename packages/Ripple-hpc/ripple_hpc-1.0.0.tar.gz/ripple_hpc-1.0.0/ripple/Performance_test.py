import numpy as np
import ase
from ase import Atoms
from ase.io import read, write
from ase.neighborlist import NeighborList
from ase.geometry.analysis import Analysis
import h5py
import os, platform
from typing import List, Tuple, Union
import warnings
import joblib
from joblib import Parallel, delayed, dump, load
import psutil
from collections import Counter
import multiprocessing
from multiprocessing import Process
from pathlib import Path
from datetime import datetime
import uuid
import timeit
import functools
from functools import partial
import statistics
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl

from static import sanity_check_multiple, chunks_create_for_rdf, memory_map, rdf_cal, rdf_core, ssf_cal, ssf_core

v=0
timestep = 0.1
N_workers = 8
target_atoms1 = 'Li'
target_atoms2 = 'Li'
target_atoms = 'Li'
N_frame = 100
r_max = 12
dr = 0.02
trajectory = ase.io.read('B:/Imperial College/PhD project - MLFF & SIC/MD_Simulation_result/MaceMD_700K_444_0vacancies_trajactory.xyz', format='extxyz', index=f'-{N_frame}:')
trajectory_tag = 'Ripple_RDF_test_worker4'
save_dir = Path('Performance_test')

def ASE_RDF_Cal(trajectory, target_atom:str, dr:float = 0.05):
    a, b, c = trajectory[0].cell 
    r_max = np.linalg.norm(np.dot(a, np.cross(b,c)))*0.5/max(np.linalg.norm(np.cross(a,b)), np.linalg.norm(np.cross(b,c)), np.linalg.norm(np.cross(c,a)))
    bins = np.arange(0, r_max+dr, dr)
    histlength = len(bins)-1
    ana = Analysis(trajectory[:])
    RDF = ana.get_rdf(rmax=r_max, nbins=histlength, elements=f'{target_atom}', return_dists=False)
    return np.mean(np.array(RDF), axis=0)

def sanity_check_multiple(trajectory, save_dir, target_atoms1, target_atoms2, N_workers):
    # check trajectory if is a list of ase.Atoms #
    if not isinstance(trajectory, list): 
        raise TypeError(f"A trajectory is a series of frames over time. The input trajectory should be a list of ase.atoms.Atoms, but got {type(trajectory)}.")
    N_frame = len(trajectory)
    if N_frame < 1:
        raise ValueError("The input trajectory is empty.")
    # check and regularize the path of the saving directory, where a temporary traj and the final h5f file will be saved #
    save_dir = Path(f"{save_dir}")
    try:
        save_dir.mkdir(parents=True, exist_ok=True) 
    except Exception as e:
        raise ValueError(f"Invalid path: {save_dir}") from e
    # check if the target_atoms existed in the trajectory #
    if (target_atoms1 not in trajectory[0].symbols) or (target_atoms2 not in trajectory[0].symbols):
        raise ValueError("The input target_atoms are not in the given trajectory.")
    # check if the N_workers is a valid input, limit the maximum number of the input N_workers #
    N_workers = int(N_workers)
    if platform.system() == "Linux":
        available = len(psutil.Process().cpu_affinity())
    else:
        available = os.cpu_count()
    if available < N_workers:
        raise ValueError(f"Only {available} CPUs are available, but user input {N_workers}.")
    if N_frame < N_workers:
        N_workers = N_frame
    return save_dir, N_frame, N_workers

def memory_map(memmap_path, traj):
    need_write = True
    if memmap_path.exists():
        mm = np.lib.format.open_memmap(memmap_path, mode='r')
        if mm.shape == traj.shape and mm.dtype == traj.dtype:
            need_write = False
        del mm
    if need_write:
        mm = np.lib.format.open_memmap(memmap_path, mode='w+', dtype=traj.dtype, shape=traj.shape)
        mm[:] = traj
        mm.flush()
        del mm            

def chunks_create_for_rdf(N_frame, N_workers):
    if N_workers == 1:
        return [np.arange(N_frame)]
    else:
        return np.array_split(np.arange(N_frame), N_workers)

def rdf_cal_test1(trajectory, trajectory_tag, save_dir, target_atoms1, target_atoms2, r_max, dr, N_workers):
    save_dir, N_frame, N_workers = sanity_check_multiple(trajectory, save_dir, target_atoms1, target_atoms2, N_workers)
    same = (target_atoms1 == target_atoms2)
    target_atoms1_index = np.array([atom.index for atom in trajectory[0] if atom.symbol==f'{target_atoms1}'])
    N_atom1 = len(target_atoms1_index)
    scale_traj1 = np.array([frame[target_atoms1_index].get_scaled_positions(wrap=False) for frame in trajectory])
    memmap_path1 = save_dir / f"temporary_info_for_rdf_{target_atoms1}_{trajectory_tag}"
    memory_map(memmap_path1, scale_traj1)
    if same:
        memmap_path2 = memmap_path1
        N_atom2 = N_atom1
    else:
        target_atoms2_index = np.array([atom.index for atom in trajectory[0] if atom.symbol==f'{target_atoms2}'])
        N_atom2 = len(target_atoms2_index)
        scale_traj2 = np.array([frame[target_atoms2_index].get_scaled_positions(wrap=False) for frame in trajectory])
        memmap_path2 = save_dir / f"temporary_info_for_rdf_{target_atoms2}_{trajectory_tag}"
        memory_map(memmap_path2, scale_traj2)
    cell = np.array(trajectory[0].cell)
    G = cell @ cell.T
    a, b, c = trajectory[0].cell 
    r_max = min(r_max, np.linalg.norm(np.dot(a, np.cross(b,c)))*0.5/max(np.linalg.norm(np.cross(a,b)), np.linalg.norm(np.cross(b,c)), np.linalg.norm(np.cross(c,a))))
    bins = np.arange(0, r_max+dr, dr)
    histlength = len(bins)-1
    distance = np.linspace(0, r_max, histlength) 
    shell_vol = (4/3)*np.pi*(bins[1:]**3 - bins[:-1]**3) # len = histlength
    V = trajectory[0].get_volume()
    lag_chunks = chunks_create_for_rdf(N_frame, N_workers)
    def rdf_core1(memmap_path1, memmap_path2, same, lag_list, bins, histlength, G):
        mm = np.lib.format.open_memmap(memmap_path1, mode='r')
        scale_traj1 = mm[lag_list]
        mm._mmap.close()
        listlength = len(lag_list) # the length of the lag time in one chunk, only determine the scale of matrix
        partial_rdf = np.zeros(histlength)
        lag_block = 100
        if same: 
            for s in range(0, listlength, lag_block):
                pos = scale_traj1[s:s+lag_block]
                diff = pos[:, None, :, :] - pos[:, :, None, :]  # shape: (lag_block, N_target, N_target, 3)
                diff -= np.round(diff)
                r2 = np.einsum('...i,ij,...j->...', diff, G, diff, optimize='greedy')
                r = np.sqrt(r2, out=r2).ravel()
                partial_rdf += np.histogram(r, bins=bins)[0]
            partial_rdf[0] = 0
        else:
            scale_traj2 = np.lib.format.open_memmap(memmap_path2, mode='r')[lag_list]
            for s in range(0, listlength, lag_block):
                pos1 = scale_traj1[s:s+lag_block]
                pos2 = scale_traj2[s:s+lag_block]
                diff = pos1[:, None, :, :] - pos2[:, :, None, :]  # shape: (lag_block, N_target1, N_target2, 3)
                diff -= np.round(diff)
                r2 = np.einsum('...i,ij,...j->...', diff, G, diff, optimize='greedy')
                r = np.sqrt(r2, out=r2).ravel()
                partial_rdf += np.histogram(r, bins=bins)[0]
        return partial_rdf
    results = Parallel(n_jobs=N_workers)(delayed(rdf_core1)(memmap_path1, memmap_path2, same, lag_list, bins, histlength, G) for lag_list in lag_chunks)
    rdf = np.zeros(histlength)
    for partial_rdf in results:
        rdf += partial_rdf
    total_rdf = rdf / (N_frame * shell_vol * N_atom1 * N_atom2 / V) # normalization
    try:
        memmap_path1.unlink(missing_ok=True)
        if not same:
            memmap_path2.unlink(missing_ok=True)
    except OSError:
        pass
    return distance, total_rdf



def rdf_cal_test2(trajectory, trajectory_tag, save_dir, target_atoms1, target_atoms2, r_max, dr, N_workers):
    save_dir = Path(f"{save_dir}")
    same = (target_atoms1 == target_atoms2)
    target_atoms1_index = np.array([atom.index for atom in trajectory[0] if atom.symbol==f'{target_atoms1}'])
    N_atom1 = len(target_atoms1_index)
    scale_traj1 = np.array([frame[target_atoms1_index].get_scaled_positions(wrap=False) for frame in trajectory])
    memmap_path1 = save_dir / f"temporary_info_for_rdf_{target_atoms1}_{trajectory_tag}"
    memory_map(memmap_path1, scale_traj1)
    if same:
        memmap_path2 = memmap_path1
        N_atom2 = N_atom1
    else:
        target_atoms2_index = np.array([atom.index for atom in trajectory[0] if atom.symbol==f'{target_atoms2}'])
        N_atom2 = len(target_atoms2_index)
        scale_traj2 = np.array([frame[target_atoms2_index].get_scaled_positions(wrap=False) for frame in trajectory])
        memmap_path2 = save_dir / f"temporary_info_for_rdf_{target_atoms2}_{trajectory_tag}"
        memory_map(memmap_path2, scale_traj2)
    cell = np.array(trajectory[0].cell)
    G = cell @ cell.T 
    a, b, c = trajectory[0].cell 
    r_max = min(r_max, np.linalg.norm(np.dot(a, np.cross(b,c)))*0.5/max(np.linalg.norm(np.cross(a,b)), np.linalg.norm(np.cross(b,c)), np.linalg.norm(np.cross(c,a))))
    r_max2 = r_max**2
    bins = np.arange(0, r_max+dr, dr)
    histlength = len(bins)-1
    distance = np.linspace(0, r_max, histlength) 
    shell_vol = (4/3)*np.pi*(bins[1:]**3 - bins[:-1]**3) # len = histlength
    V = trajectory[0].get_volume()
    lag_chunks = chunks_create_for_rdf(N_frame, N_workers)
    def rdf_core2(memmap_path1, memmap_path2, same, lag_list, bins, histlength, r_max2, G):
        scale_traj1 = np.lib.format.open_memmap(memmap_path1, mode='r')[lag_list]
        listlength = len(lag_list) # the length of the lag time in one chunk, only determine the scale of matrix
        partial_rdf = np.zeros(histlength)
        lag_block = 100
        if same: 
            for s in range(0, listlength, lag_block):
                pos = scale_traj1[s:s+lag_block]
                diff = pos[:, None, :, :] - pos[:, :, None, :]  # shape: (lag_block, N_target, N_target, 3)
                diff -= np.round(diff)
                r2 = np.einsum('...i,ij,...j->...', diff, G, diff, optimize=True)
                r = np.sqrt(r2[r2 <= r_max2])
                idx = np.searchsorted(bins, r, side='right') - 1   # safe & correct
                np.clip(idx, 0, histlength - 1, out=idx)
                np.add.at(partial_rdf, idx, 1)
        else:
            scale_traj2 = np.lib.format.open_memmap(memmap_path2, mode='r')[lag_list]
            for s in range(0, listlength, lag_block):
                pos1 = scale_traj1[s:s+lag_block]
                pos2 = scale_traj2[s:s+lag_block]
                diff = pos1[:, None, :, :] - pos2[:, :, None, :]  # shape: (lag_block, N_target1, N_target2, 3)
                diff -= np.round(diff)
                r2 = np.einsum('...i,ij,...j->...', diff, G, diff, optimize=True)
                r = np.sqrt(r2, out=r2).ravel()
                partial_rdf += np.histogram(r, bins=bins)[0]
        partial_rdf[0] = 0
        return partial_rdf
    results = Parallel(n_jobs=N_workers)(delayed(rdf_core2)(memmap_path1, memmap_path2, same, lag_list, bins, histlength, r_max2, G) for lag_list in lag_chunks)
    rdf = np.zeros(histlength)
    for partial_rdf in results:
        rdf += partial_rdf
    total_rdf = rdf / (N_frame * shell_vol * N_atom1 * N_atom2 / V) # normalization
    dk = np.pi/r_max/10                     # need to update
    k_space = np.arange(0, 6, dk) # need to update
    total_ssf = np.zeros(len(k_space))
    for k in range(1,len(k_space)): # Fourier transformation to obtain static structure factors
        total_ssf[k] = 1 + 4*np.pi*(N_atom2/V)* np.sum(distance * (total_rdf-1) * np.sin(k_space[k]*distance) / k_space[k] * dr, axis=0)
    try:
        memmap_path1.unlink(missing_ok=True)
        if not same:
            memmap_path2.unlink(missing_ok=True)
    except OSError:
        pass
    return k_space, total_ssf


import freud
import mdtraj
trajectory = ase.io.read('B:/Imperial College/PhD project - MLFF & SIC/MD_Simulation_result/MaceMD_700K_444_0vacancies_trajactory.xyz', format='extxyz', index='-100:')

def freud_rdf_test(trajectory, target_atoms, r_max, bins):
    rdf = freud.density.RDF(bins=bins, r_max=r_max, normalization_mode='finite_size')
    g_r = np.zeros(bins)
    target_atoms_index = np.array([atom.index for atom in trajectory[0] if atom.symbol==f'{target_atoms}'])
    for frame in trajectory:
        box = freud.box.Box.from_matrix(frame.cell.T)
        positions = frame[target_atoms_index].get_positions(wrap=True)
        rdf.compute(system=(box, positions), reset=True)
        r = rdf.bin_centers
        g_r += rdf.rdf
    return g_r / len(trajectory)

test1 = rdf_cal_test1(trajectory, 'Ripple_RDF_test_worker4', save_dir, target_atoms1, target_atoms2, r_max, dr, N_workers)
test3 = freud_rdf_test(trajectory, target_atoms1, r_max=11.48, bins=550)
plt.plot(test1[0],test1[1])
plt.show()

test_rdf_ssf_k, test_rdf_ssf = rdf_cal_test2(trajectory, 'Ripple_RDF_test_worker4', save_dir, target_atoms1, target_atoms2, r_max, dr, N_workers)
plt.plot(test_rdf_ssf_k, test_rdf_ssf)
plt.show()


# test accuracy
standard = ASE_RDF_Cal(trajectory, target_atoms1, dr=0.02)
test1 = rdf_cal_test1(trajectory, 'Ripple_RDF_test_worker4', save_dir, target_atoms1, target_atoms2, r_max, dr, N_workers)
test2 = rdf_cal_test2(trajectory, 'Ripple_RDF_test_worker4', save_dir, target_atoms1, target_atoms2, r_max, dr, N_workers)


font_path = fm.findfont(fm.FontProperties(family='Times New Roman'))
font = fm.FontProperties(fname=font_path, size=16)
fig = plt.figure("plot", figsize=(9, 7), dpi=100)
plt.subplots_adjust(top=0.95, bottom=0.105, left=0.13, right=0.98, hspace=0.05, wspace=0.05)
fig.tight_layout(pad=0.0)
ax = fig.add_subplot(111)
ax.plot(test1, label='Ripple1')
ax.plot(test2, label='Ripple2')
#ax.plot(distance, standard, label='ASE')
file.close()
ax.set_ylabel('g(r)', fontproperties=font)
ax.set_xlabel('Distance (Å)', fontproperties=font)
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 16
ax.tick_params(axis='both', which='both', direction='inout', length=5.0, width=2.0, color='black')
ax.legend(loc='lower right', fontsize=14, frameon=True)
fig.show()

mean_Ripple = []; std_Ripple = []
wrapped = partial(rdf_cal_test1, trajectory[0:10], 'Ripple_RDF_test_worker4', save_dir, target_atoms1, target_atoms2, r_max, dr, N_workers=16)
runs = timeit.repeat(wrapped, number=1, repeat=10)
mean_Ripple.append(statistics.mean(runs)); std_Ripple.append(statistics.stdev(runs))
wrapped = partial(rdf_cal_test1, trajectory[0:20], 'Ripple_RDF_test_worker4', save_dir, target_atoms1, target_atoms2, r_max, dr, N_workers=16)
runs = timeit.repeat(wrapped, number=1, repeat=10)
mean_Ripple.append(statistics.mean(runs)); std_Ripple.append(statistics.stdev(runs))
wrapped = partial(rdf_cal_test1, trajectory[0:30], 'Ripple_RDF_test_worker4', save_dir, target_atoms1, target_atoms2, r_max, dr, N_workers=16)
runs = timeit.repeat(wrapped, number=1, repeat=10)
mean_Ripple.append(statistics.mean(runs)); std_Ripple.append(statistics.stdev(runs))
wrapped = partial(rdf_cal_test1, trajectory[0:40], 'Ripple_RDF_test_worker4', save_dir, target_atoms1, target_atoms2, r_max, dr, N_workers=16)
runs = timeit.repeat(wrapped, number=1, repeat=10)
mean_Ripple.append(statistics.mean(runs)); std_Ripple.append(statistics.stdev(runs))
wrapped = partial(rdf_cal_test1, trajectory[0:50], 'Ripple_RDF_test_worker4', save_dir, target_atoms1, target_atoms2, r_max, dr, N_workers=16)
runs = timeit.repeat(wrapped, number=1, repeat=10)
mean_Ripple.append(statistics.mean(runs)); std_Ripple.append(statistics.stdev(runs))
wrapped = partial(rdf_cal_test1, trajectory[0:60], 'Ripple_RDF_test_worker4', save_dir, target_atoms1, target_atoms2, r_max, dr, N_workers=16)
runs = timeit.repeat(wrapped, number=1, repeat=10)
mean_Ripple.append(statistics.mean(runs)); std_Ripple.append(statistics.stdev(runs))
wrapped = partial(rdf_cal_test1, trajectory[0:70], 'Ripple_RDF_test_worker4', save_dir, target_atoms1, target_atoms2, r_max, dr, N_workers=16)
runs = timeit.repeat(wrapped, number=1, repeat=10)
mean_Ripple.append(statistics.mean(runs)); std_Ripple.append(statistics.stdev(runs))

mean_freud = []; std_freud = []
wrapped = partial(freud_rdf_test, trajectory[0:10], target_atoms1, 11.48, 550)
runs = timeit.repeat(wrapped, number=1, repeat=10)
mean_freud.append(statistics.mean(runs)); std_freud.append(statistics.stdev(runs))
wrapped = partial(freud_rdf_test, trajectory[0:20], target_atoms1, 11.48, 550)
runs = timeit.repeat(wrapped, number=1, repeat=10)
mean_freud.append(statistics.mean(runs)); std_freud.append(statistics.stdev(runs))
wrapped = partial(freud_rdf_test, trajectory[0:30], target_atoms1, 11.48, 550)
runs = timeit.repeat(wrapped, number=1, repeat=10)
mean_freud.append(statistics.mean(runs)); std_freud.append(statistics.stdev(runs))
wrapped = partial(freud_rdf_test, trajectory[0:40], target_atoms1, 11.48, 550)
runs = timeit.repeat(wrapped, number=1, repeat=10)
mean_freud.append(statistics.mean(runs)); std_freud.append(statistics.stdev(runs))
wrapped = partial(freud_rdf_test, trajectory[0:50], target_atoms1, 11.48, 550)
runs = timeit.repeat(wrapped, number=1, repeat=10)
mean_freud.append(statistics.mean(runs)); std_freud.append(statistics.stdev(runs))
wrapped = partial(freud_rdf_test, trajectory[0:60], target_atoms1, 11.48, 550)
runs = timeit.repeat(wrapped, number=1, repeat=10)
mean_freud.append(statistics.mean(runs)); std_freud.append(statistics.stdev(runs))
wrapped = partial(freud_rdf_test, trajectory[0:70], target_atoms1, 11.48, 550)
runs = timeit.repeat(wrapped, number=1, repeat=10)
mean_freud.append(statistics.mean(runs)); std_freud.append(statistics.stdev(runs))

plt.errorbar([10,20,30,40,50,60,70], mean_freud, yerr=std_freud, label = 'Average freud run-time')
plt.errorbar([10,20,30,40,50,60,70], mean_Ripple, yerr=std_Ripple, label = 'Average Ripple run-time with 16 cores')
plt.xticks([10,20,30,40,50,60,70]) 
plt.xlabel("Number of frames (896 particles per frame)")
plt.ylabel("Average run time (s)")
plt.tight_layout()
plt.legend()
plt.show()




wrapped = partial(ASE_RDF_Cal, trajectory[0:10], target_atoms1, dr)
wrapped = partial(ASE_RDF_Cal, trajectory[0:20], target_atoms1, dr)
wrapped = partial(ASE_RDF_Cal, trajectory[0:30], target_atoms1, dr)
wrapped = partial(ASE_RDF_Cal, trajectory[0:40], target_atoms1, dr)
wrapped = partial(ASE_RDF_Cal, trajectory[0:50], target_atoms1, dr)


mean_ASE = []; mean_Ripple = []
std_ASE = []; std_Ripple = []
for f in [wrap_ASE_RDF_Cal_0,wrap_ASE_RDF_Cal_1,wrap_ASE_RDF_Cal_2,wrap_ASE_RDF_Cal_3,wrap_ASE_RDF_Cal_4,wrap_ASE_RDF_Cal_5]:
    timer = timeit.Timer(f)
    runs = timer.repeat(repeat=10, number=1)
    mean_ASE.append(statistics.mean(runs)) # [2.17397573000635, 22.110966660000848, 41.08976796000498, 59.313879599986834, 80.80662681999965, 101.62510396999423]
    std_ASE.append(statistics.stdev(runs)) # [0.05606054959238196, 0.4989950743700668, 2.0921036753113285, 2.3484614795345835, 1.524144499375138, 1.082133612195958]

for f in [wrap_Ripple_rdf_test_0,wrap_Ripple_rdf_test_1,wrap_Ripple_rdf_test_2,wrap_Ripple_rdf_test_3,wrap_Ripple_rdf_test_4,wrap_Ripple_rdf_test_5]:
    timer = timeit.Timer(f)
    runs = timer.repeat(repeat=10, number=1)
    mean_Ripple.append(statistics.mean(runs))
    std_Ripple.append(statistics.stdev(runs))
    

plt.errorbar([1,10,20,30,40,50], mean_ASE, yerr=std_ASE, label = 'Average ASE run-time')
plt.errorbar([1,10,20,30,40,50], mean_Ripple, yerr=std_Ripple, label = 'Average Ripple run-time with 16 cores')
plt.xticks([1,10,20,30,40,50]) 
plt.xlabel("Number of frames (896 particles per frame)")
plt.ylabel("Average run time (s)")
plt.tight_layout()
plt.legend()
plt.show()

mean_Ripple = []; std_Ripple = []
wrapped = partial(rdf_cal, trajectory[0:1000], 'Ripple_RDF_test_worker1', save_dir, target_atoms1, target_atoms2, r_max, dr, N_workers=1)
wrapped = partial(rdf_cal, trajectory[0:1000], 'Ripple_RDF_test_worker2', save_dir, target_atoms1, target_atoms2, r_max, dr, N_workers=2)
wrapped = partial(rdf_cal, trajectory[0:1000], 'Ripple_RDF_test_worker4', save_dir, target_atoms1, target_atoms2, r_max, dr, N_workers=4)
wrapped = partial(rdf_cal, trajectory[0:1000], 'Ripple_RDF_test_worker4', save_dir, target_atoms1, target_atoms2, r_max, dr, N_workers=6)
wrapped = partial(rdf_cal, trajectory[0:1000], 'Ripple_RDF_test_worker4', save_dir, target_atoms1, target_atoms2, r_max, dr, N_workers=8)


runs = timeit.repeat(wrapped, number=1, repeat=10)
mean_Ripple.append(statistics.mean(runs)) # [282.9870998499995, 134.23890593000252, 66.66537468000169, 44.18798986000329, 37.49396629000112]
std_Ripple.append(statistics.stdev(runs)) # [4.880382028327523, 0.8161205680899835, 1.553145027108312, 1.4849442776868864, 5.176761169137675]

plt.errorbar([1,2,4,6,8], mean_Ripple, yerr=std_Ripple, label = 'Average Ripple run-time on 1000 frames')
plt.xticks([1,2,4,6,8]) 
plt.xlabel("Number of cores to do parallel computation")
plt.ylabel("Average run time (s)")
plt.tight_layout()
plt.legend()
plt.show()
#------------------------------------------------------------------#


def chunks_create_for_ssf(N_frame, N_workers):
    if N_workers == 1:
        return [slice(0, N_frame)]
    else:
        base = N_frame // N_workers
        remainder = N_frame % N_workers
        slices = []
        start = 0
        for i in range(N_workers):
            length = base + (1 if i < remainder else 0)
            stop = start + length
            slices.append(slice(start, stop))
            start = stop
    return slices

def ssf_cal(trajectory, trajectory_tag, save_dir, k_max, dk_shell, target_atoms1, target_atoms2, N_workers):
    save_dir = Path(f"{save_dir}")
    same = (target_atoms1 == target_atoms2)
    target_atoms1_index = np.array([atom.index for atom in trajectory[0] if atom.symbol==f'{target_atoms1}'])
    N_atom1 = len(target_atoms1_index)
    traj1 = np.array([frame[target_atoms1_index].get_positions(wrap=False) for frame in trajectory])
    memmap_path1 = save_dir / f"temporary_info_for_ssf_{target_atoms1}_{trajectory_tag}"
    memory_map(memmap_path1, traj1)
    if same:
        memmap_path2 = memmap_path1
        N_atom2 = N_atom1
    else:
        target_atoms2_index = np.array([atom.index for atom in trajectory[0] if atom.symbol==f'{target_atoms2}'])
        N_atom2 = len(target_atoms2_index)
        traj2 = np.array([frame[target_atoms2_index].get_positions(wrap=True) for frame in trajectory])
        memmap_path2 = save_dir / f"temporary_info_for_ssf_{target_atoms2}_{trajectory_tag}"
        memory_map(memmap_path2, traj2)
    V = trajectory[0].get_volume()
    a, b, c = trajectory[0].cell 
    b1 = 2 * np.pi * np.cross(b, c) / V  # reciprocal basis
    b2 = 2 * np.pi * np.cross(c, a) / V
    b3 = 2 * np.pi * np.cross(a, b) / V
    B = np.vstack([b1, b2, b3])          # B = (3,3) reciprocal basis
    hmax = int(np.ceil(k_max / np.linalg.norm(b1)))
    kmax = int(np.ceil(k_max / np.linalg.norm(b2)))
    lmax = int(np.ceil(k_max / np.linalg.norm(b3)))       
    grid = np.array(np.meshgrid(np.arange(-hmax, hmax+1), np.arange(-kmax, kmax+1), np.arange(-lmax, lmax+1), indexing='ij')).reshape(3,-1).T 
    k_vec_raw = grid @ B
    k_mod_raw = np.linalg.norm(k_vec_raw, axis=1)   # (Nk,)
    mask = (k_mod_raw > 0) & (k_mod_raw < k_max)
    k_vec = k_vec_raw[mask]  # (Nk,3)
    k_mod = k_mod_raw[mask]
    shell = (k_mod / dk_shell).astype(int)     # (Nk,)  
    Nshell   = shell.max() + 1
    k_mid = (np.arange(Nshell)+0.5)*dk_shell
    lag_chunks = chunks_create_for_ssf(N_frame, N_workers)
    def ssf_core(memmap_path1, memmap_path2, lag_list, same, k_vec):
        pos_a = np.lib.format.open_memmap(memmap_path1, mode='r')[lag_list] # (N_lag, N_atom1, 3)
        N_lag, N_atom1, N_dim = pos_a.shape
        if same:
            pos_b = pos_a
            N_atom2 = N_atom1
        else:
            pos_b = np.lib.format.open_memmap(memmap_path2, mode='r')[lag_list]
            N_lag, N_atom2, N_dim = pos_b.shape
        Nk = len(k_vec)
        sqrtN  = np.sqrt(N_atom1*N_atom2)
        Sab_k  = np.zeros(Nk)
        k_batch = 2048
        for s in range(0, Nk, k_batch):
            end = min(s+k_batch, Nk)
            k_b = k_vec[s:end]  # k_b is k_batch, batch length is b
            phase_a = np.tensordot(k_b, pos_a, axes=([1], [2])) # (k_b.shape[0], N_lag, N_atom1)
            rho_a = np.exp(1j * phase_a).sum(axis=2) # (b, N_lag)
            if same:
                Sab_frame = (rho_a.conj() * rho_a).real / sqrtN # (C_a**2 + S_a**2) / sqrtN
            else:
                phase_b = np.tensordot(k_b, pos_b, axes=([1],[2]))
                rho_b   = np.exp(1j * phase_b).sum(axis=2)
                Sab_frame = (rho_a.conj() * rho_b).real / sqrtN # (C_a*C_b + S_a*S_b) / sqrtN
            Sab_k[s:end] = Sab_frame.sum(axis=1)        # sum over N_lag then take average outside
        return Sab_k
    results = Parallel(n_jobs=N_workers, backend="loky")(delayed(ssf_core)(memmap_path1, memmap_path2, lag_list, same, k_vec) for lag_list in lag_chunks)
    ssf = np.zeros(len(k_vec))
    for partial_ssf in results:
        ssf = ssf + partial_ssf
    ssf = ssf / N_frame
    ssf_shell = np.bincount(shell, weights=ssf, minlength=Nshell)
    cnt_shell = np.bincount(shell, minlength=Nshell)
    ssf_shell /= np.maximum(cnt_shell, 1)
    try:
        memmap_path1.unlink(missing_ok=True)
        if not same:
            memmap_path2.unlink(missing_ok=True)
    except OSError:
        pass
    return k_mid, ssf_shell


trajectory = ase.io.read('B:/Imperial College/PhD project - MLFF & SIC/MD_Simulation_result/MaceMD_700K_444_0vacancies_trajactory.xyz', format='extxyz', index=f'-{N_frame}:')
v=0
timestep = 0.1
N_workers = 10
target_atoms1 = 'Li'
target_atoms2 = 'Li'
N_frame = 100
r_max = 12
dr = 0.02
trajectory_tag = 'Ripple_RDF_test_worker4'
save_dir = Path('Performance_test')
k_max = 5
dk_shell = 0.1
k_mid, test_ssf = ssf_cal(trajectory, 'Ripple_SSF_test_worker4', save_dir, k_max, dk_shell, target_atoms1, target_atoms2, N_workers)
k_mid2, test_ssf2 = ssf_cal(trajectory, 'Ripple_SSF_test_worker4', save_dir, k_max, dk_shell, target_atoms1, target_atoms2, N_workers)

test_rdf_ssf_k, test_rdf_ssf = rdf_cal_test2(trajectory, 'Ripple_RDF_test_worker4', save_dir, target_atoms1, target_atoms2, r_max, dr, N_workers)

plt.plot(test_rdf_ssf_k, test_rdf_ssf)
plt.plot(k_mid, test_ssf)
plt.plot(k_mid2, test_ssf2)
plt.show()

##############################     VERY IMPORTANT : Freud!    ############################################
import freud
import mdtraj
trajectory = ase.io.read('B:/Imperial College/PhD project - MLFF & SIC/MD_Simulation_result/MaceMD_700K_444_0vacancies_trajactory.xyz', format='extxyz', index='-100:')
rdf = freud.density.RDF(bins=550, r_max=11.0, normalization_mode='finite_size')
g_r = np.zeros(550)
target_atoms1_index = np.array([atom.index for atom in trajectory[0] if atom.symbol==f'{target_atoms1}'])
for frame in trajectory:
    box = freud.box.Box.from_matrix(frame.cell.T)
    positions = frame[target_atoms1_index].get_positions(wrap=True)
    rdf.compute(system=(box, positions), reset=True)
    r = rdf.bin_centers
    g_r += rdf.rdf

g_r /= len(trajectory)
plt.plot(r,g_r)

test1 = rdf_cal_test1(trajectory, 'Ripple_RDF_test_worker4', save_dir, target_atoms1, target_atoms2, r_max, dr, N_workers)
plt.plot(test1[0],test1[1])
plt.show()



bins = 100
k_max = 5
k_min = 0.2
S_k_direct = np.zeros(bins)
S_k_debye = np.zeros(bins)
sfDirect = freud.diffraction.StaticStructureFactorDirect(bins=bins, k_max=k_max, k_min=k_min)
sfDebye = freud.diffraction.StaticStructureFactorDebye(num_k_values=bins, k_max=k_max, k_min=k_min)
for frame in trajectory:
    box = freud.box.Box.from_matrix(frame.cell.T)
    positions = frame[target_atoms1_index].get_positions(wrap=True)
    sfDirect.compute(system=(box, positions), query_points=positions, N_total=len(target_atoms1_index), reset=True)
    r_direct = sfDirect.bin_centers
    S_k_direct += sfDirect.S_k
    sfDebye.compute(system=(box, positions), query_points=positions, N_total=len(target_atoms1_index), reset=True)
    r_debye = sfDebye.k_values
    S_k_debye += sfDebye.S_k

plt.plot(r_direct, S_k_direct/len(trajectory), label="Direct")
plt.plot(r_debye, S_k_debye/len(trajectory), label="Debye")
#plt.plot(test_rdf_ssf_k, test_rdf_ssf, label='custom_rdf>ssf')
plt.plot(k_mid, test_ssf, label='custom_ssf')
plt.legend()
plt.show()


##### DINASOUR ##################


import numpy as np
import matplotlib.pyplot as plt
from ase.io import read, write
import dynasor
from dynasor.qpoints import get_spherical_qpoints
from dynasor import compute_static_structure_factors, Trajectory
from dynasor.post_processing import get_spherically_averaged_sample_smearing
from dynasor.post_processing import get_spherically_averaged_sample_binned
N_frame = 100
trajectory = ase.io.read('B:/Imperial College/PhD project - MLFF & SIC/MD_Simulation_result/MaceMD_700K_444_0vacancies_trajactory.xyz', format='extxyz', index=f'{-N_frame}:')
target_atoms1_index = np.array([atom.index for atom in trajectory[0] if atom.symbol==f'{target_atoms1}'])
atomic_indices = trajectory[0].symbols.indices()
key = 'Li'
subset_indices = {key: atomic_indices[key]}

traj = Trajectory('B:/Imperial College/PhD project - MLFF & SIC/MD_Simulation_result/MaceMD_700K_444_0vacancies_trajactory.xyz', 
                  trajectory_format='extxyz', 
                  atomic_indices=subset_indices, 
                  length_unit='Angstrom',
                  time_unit='fs',
                  frame_step=1,
                  frame_stop=100)
q_max = 5
q_linspace = np.linspace(0, q_max, 100)
q_points = get_spherical_qpoints(traj.cell, q_max)
sample = compute_static_structure_factors(traj, q_points)
sample_averaged = get_spherically_averaged_sample_smearing(sample, q_norms=q_linspace, q_width=0.01)
q_norms = sample_averaged.q_norms
plt.plot(q_norms[20:], sample_averaged.Sq[20:]*2688/896, label="Dynasor") #  / len(subset_indices['Li'])
plt.plot(r_direct[7:], S_k_direct[7:]/len(trajectory), label="Freud Direct")
plt.plot(r_debye[7:], S_k_debye[7:]/len(trajectory), label="Freud Debye")
#plt.plot(test_rdf_ssf_k, test_rdf_ssf, label='custom_rdf>ssf')
plt.plot(k_mid, test_ssf, label='Ripple')
plt.legend()
plt.show()





