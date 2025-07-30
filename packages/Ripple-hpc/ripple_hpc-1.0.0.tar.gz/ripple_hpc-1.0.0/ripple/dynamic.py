import numpy as np
import ase
from ase import Atoms
from ase.io import read, write
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

def sanity_check(trajectory, save_dir, target_atoms, N_workers):
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
    if target_atoms not in trajectory[0].symbols:
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

def dynamic_chunks_create(N_frame, N_workers):
    if N_workers == 1:
        return [np.arange(N_frame)]
    lag_chunks = []
    for i in range(N_workers-1):
        lag_chunks.append(N_frame-1 - np.arange(int((i/N_workers)**0.5 * N_frame), int(((i+1)/N_workers)**0.5 * N_frame)))
    lag_chunks.append(np.arange(lag_chunks[-1][-1]-1, -1, -1))
    lag_chunks = [sublist for sublist in lag_chunks if sublist.size != 0]
    lag_chunks = [i[::-1] for i in lag_chunks[::-1]]
    return lag_chunks

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

#def block_estimate(traj_corrected):
#    ram_traj = len(traj_corrected.flatten())*8/1024**3 #Gb

def msd_cal(trajectory:List["ase.atoms.Atoms"],
            trajectory_tag:str,
            save_dir:str,
            target_atoms:str,
            timestep:float,
            N_workers: int = 4):
    """
    trajectory_tag is used to ensure the uniqueness of the output file.
    traj.shape = (N_frame, N_atom, dimensions)
    total lag time depends on the given trajectory (ase.atoms.Atoms)
    split lag time to do parallel calculation
    """
    save_dir, N_frame, N_workers = sanity_check(trajectory, save_dir, target_atoms, N_workers)
    target_atom_index = np.array([atom.index for atom in trajectory[0] if atom.symbol==f'{target_atoms}'])
    N_atom = len(target_atom_index)
    traj = np.stack([frame[target_atom_index].get_positions(wrap=False) for frame in trajectory], axis=0)
    framework_index = np.delete(np.arange(len(trajectory[0])), target_atom_index)
    framework = np.mean(np.array([frame[framework_index].get_positions(wrap=False) for frame in trajectory]), axis=1)
    traj_corrected = traj - framework[:, None]
    memmap_path = save_dir / f"temporary_info_for_{target_atoms}_msd_{trajectory_tag}"
    memory_map(memmap_path, traj_corrected)
    del traj_corrected
    lag_chunks = dynamic_chunks_create(N_frame, N_workers)
    N_workers = len(lag_chunks)
    def msd_core(memmap_path, lag_list, N_frame, N_atom):
        traj_corrected = np.lib.format.open_memmap(memmap_path, mode='r')
        partial_msd = np.zeros([7, len(lag_list)]) # xyz, xy, xz, yz, x, y, z #
        for index, lag in enumerate(lag_list):
            count = N_frame - lag
            block = max(1, min(4000, count))
            for beg in range(0, count, block):
                end = min(beg+block, count)
                dis = traj_corrected[beg+lag:end+lag] - traj_corrected[beg:end]
                dis2 = dis**2
                dx2 = dis2[:,:,0].sum(1)
                dy2 = dis2[:,:,1].sum(1)
                dz2 = dis2[:,:,2].sum(1)
                partial_msd[0, index] += (dx2 + dy2 + dz2).sum()
                partial_msd[1, index] += (dx2 + dy2).sum()
                partial_msd[2, index] += (dx2 + dz2).sum()
                partial_msd[3, index] += (dy2 + dz2).sum()
                partial_msd[4, index] += dx2.sum()
                partial_msd[5, index] += dy2.sum()
                partial_msd[6, index] += dz2.sum()
            partial_msd[:, index] /= count
        del traj_corrected
        return lag_list[0], partial_msd/N_atom
    results = Parallel(n_jobs=N_workers, backend="loky")(delayed(msd_core)(memmap_path, lag_list, N_frame, N_atom) for lag_list in lag_chunks)
    msd = np.zeros([7, N_frame])
    for lag_start, partial_msd in results:
        msd[:, lag_start: lag_start + partial_msd.shape[1]] = partial_msd
    D_sigma = 
    h5f_path = save_dir / f"msd_{target_atoms}_{trajectory_tag}.hdf5" # h5f file contains all calculated results #
    datasets = {"TIME": np.arange(N_frame)*timestep,
                "MSD_xyz": msd[0],
                "MSD_xy": msd[1],
                "MSD_xz": msd[2],
                "MSD_yz": msd[3],
                "MSD_x": msd[4],
                "MSD_y": msd[5],
                "MSD_z": msd[6]}
    with h5py.File(h5f_path, "a") as h5f:
        for name, data in datasets.items():
            if name in h5f: del h5f[name]
            h5f.create_dataset(name, data=data)
    try:
        memmap_path.unlink(missing_ok=True)
    except OSError:
        pass



def cmsd_cal(trajectory:List["ase.atoms.Atoms"],
            trajectory_tag:str,
            save_dir:str,
            target_atoms:str,
            timestep:float,
            N_workers: int = 4):
    """
    trajectory_tag is used to ensure the uniqueness of the output file.
    traj.shape = (N_frame, N_atom, dimensions)
    total lag time depends on the given trajectory (ase.atoms.Atoms)
    split lag time to do parallel calculation
    """
    save_dir, N_frame, N_workers = sanity_check(trajectory, save_dir, target_atoms, N_workers)
    target_atom_index = np.array([atom.index for atom in trajectory[0] if atom.symbol==f'{target_atoms}'])
    N_atom = len(target_atom_index)
    traj = np.stack([frame[target_atom_index].get_positions(wrap=False) for frame in trajectory], axis=0)
    framework_index = np.delete(np.arange(len(trajectory[0])), target_atom_index)
    framework = np.mean(np.array([frame[framework_index].get_positions(wrap=False) for frame in trajectory]), axis=1)
    traj_corrected = traj - framework[:, None]
    memmap_path = save_dir / f"temporary_info_for_{target_atoms}_cmsd_{trajectory_tag}" # define the path of the shared huge array #
    memory_map(memmap_path, traj_corrected)
    del traj_corrected
    lag_chunks = dynamic_chunks_create(N_frame, N_workers)
    N_workers = len(lag_chunks)
    def cmsd_core(memmap_path, lag_list, N_frame, N_atom):
        traj_corrected = np.lib.format.open_memmap(memmap_path, mode='r')
        partial_cmsd = np.zeros([7, len(lag_list)]) # xyz, xy, xz, yz, x, y, z #
        for index, lag in enumerate(lag_list):
            count = N_frame - lag
            block = max(1, min(4000, count))
            for beg in range(0, count, block):
                end = min(beg+block, count)
                dis = traj_corrected[beg+lag:end+lag] - traj_corrected[beg:end]
                dis_center2 = dis.sum(1)**2
                partial_cmsd[0, index] += dis_center2.sum()
                partial_cmsd[1, index] += dis_center2[:,[0,1]].sum()
                partial_cmsd[2, index] += dis_center2[:,[0,2]].sum()
                partial_cmsd[3, index] += dis_center2[:,[1,2]].sum()
                partial_cmsd[4, index] += dis_center2[:, 0].sum()
                partial_cmsd[5, index] += dis_center2[:, 1].sum()
                partial_cmsd[6, index] += dis_center2[:, 2].sum()
            partial_cmsd[:, index] /= count
        del traj_corrected
        return lag_list[0], partial_cmsd/N_atom
    results = Parallel(n_jobs=N_workers, backend="loky")(delayed(cmsd_core)(memmap_path, lag_list, N_frame, N_atom) for lag_list in lag_chunks)
    cmsd = np.zeros([7, N_frame])
    for lag_start, partial_cmsd in results:
        cmsd[:, lag_start: lag_start + partial_cmsd.shape[1]] = partial_cmsd
    h5f_path = save_dir / f"cmsd_{target_atoms}_{trajectory_tag}.hdf5" # h5f file contains all calculated results #
    datasets = {"TIME": np.arange(N_frame)*timestep,
                "cMSD_xyz": cmsd[0],
                "cMSD_xy": cmsd[1],
                "cMSD_xz": cmsd[2],
                "cMSD_yz": cmsd[3],
                "cMSD_x": cmsd[4],
                "cMSD_y": cmsd[5],
                "cMSD_z": cmsd[6]}
    with h5py.File(h5f_path, "a") as h5f:
        for name, data in datasets.items():
            if name in h5f: del h5f[name]
            h5f.create_dataset(name, data=data)
    try:
        memmap_path.unlink(missing_ok=True)
    except OSError:
        pass




def cross_corre_cal(trajectory:List["ase.atoms.Atoms"],
                    trajectory_tag:str,
                    save_dir:str,
                    target_atoms:str,
                    timestep:float,
                    N_workers: int = 4):
    """
    trajectory_tag is used to ensure the uniqueness of the output file.
    traj.shape = (N_frame, N_atom, dimensions)
    total lag time depends on the given trajectory (ase.atoms.Atoms)
    split lag time to do parallel calculation
    """
    save_dir, N_frame, N_workers = sanity_check(trajectory, save_dir, target_atoms, N_workers)
    target_atom_index = np.array([atom.index for atom in trajectory[0] if atom.symbol==f'{target_atoms}'])
    N_atom = len(target_atom_index)
    traj = np.stack([frame[target_atom_index].get_positions(wrap=False) for frame in trajectory], axis=0)
    framework_index = np.delete(np.arange(len(trajectory[0])), target_atom_index)
    framework = np.mean(np.array([frame[framework_index].get_positions(wrap=False) for frame in trajectory]), axis=1)
    traj_corrected = traj - framework[:, None]
    memmap_path = save_dir / f"temporary_info_for_{target_atoms}_crosscorrelation_{trajectory_tag}" # define the path of the shared huge array #
    memory_map(memmap_path, traj_corrected)
    del traj_corrected
    lag_chunks = dynamic_chunks_create(N_frame, N_workers)
    N_workers = len(lag_chunks)
    def cross_corre_core(memmap_path, lag_list, N_frame, N_atom):
        traj_corrected = np.lib.format.open_memmap(memmap_path, mode='r')
        partial_results = np.zeros([7, len(lag_list)]) # xyz, xy, xz, yz, x, y, z #
        for index, lag in enumerate(lag_list):
            count = N_frame - lag # number of frames to do time average #
            block = max(1, min(4000, count))
            for beg in range(0, count, block):
                end = min(beg+block, count)
                dis = traj_corrected[beg+lag:end+lag] - traj_corrected[beg:end]  # (lag, N_atom, 3) #
                #inner_prod = dis[:, pair_indices[:, 0], :] * dis[:, pair_indices[:, 1], :] #  (d1*d2).shape (n_pairs, 3) #
                sx  = dis[:,:,0].sum(1);  sx2  = (dis[:,:,0]**2).sum(1)
                sy  = dis[:,:,1].sum(1);  sy2  = (dis[:,:,1]**2).sum(1)
                sz  = dis[:,:,2].sum(1);  sz2  = (dis[:,:,2]**2).sum(1)
                ox = sx**2 - sx2
                oy = sy**2 - sy2
                oz = sz**2 - sz2
                partial_results[0, index] += np.sum(ox + oy + oz)
                partial_results[1, index] += np.sum(ox + oy)
                partial_results[2, index] += np.sum(ox + oz)
                partial_results[3, index] += np.sum(oy + oz)
                partial_results[4, index] += np.sum(ox)
                partial_results[5, index] += np.sum(oy)
                partial_results[6, index] += np.sum(oz)
            partial_results[:, index] /= count # time average, not yet divided by N_atom #
        del traj_corrected
        return lag_list[0], partial_results/N_atom
    results = Parallel(n_jobs=N_workers, backend="loky")(delayed(cross_corre_core)(memmap_path, lag_list, N_frame, N_atom) for lag_list in lag_chunks)
    cross_correlation = np.zeros([7, N_frame])
    for lag_start, partial_result in results:
        cross_correlation[:, lag_start : lag_start+partial_result.shape[1]] = partial_result
    h5f_path = save_dir / f"crosscorrelation_{target_atoms}_{trajectory_tag}.hdf5" # h5f file contains all calculated results #
    datasets = {"TIME": np.arange(N_frame)*timestep,
                "cross_correlation_xyz": cross_correlation[0],
                "cross_correlation_xy": cross_correlation[1],
                "cross_correlation_xz": cross_correlation[2],
                "cross_correlation_yz": cross_correlation[3],
                "cross_correlation_x": cross_correlation[4],
                "cross_correlation_y": cross_correlation[5],
                "cross_correlation_z": cross_correlation[6]}
    with h5py.File(h5f_path, "a") as h5f:
        for name, data in datasets.items():
            if name in h5f: del h5f[name]
            h5f.create_dataset(name, data=data)
    try:
        memmap_path.unlink(missing_ok=True)
    except OSError:
        pass


