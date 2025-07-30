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


def vhf_distinct_cal(trajectory:List["ase.atoms.Atoms"],
                     trajectory_tag:str,
                     save_dir:str,
                     target_atoms1:str,
                     target_atoms2:str,
                     r_max:float = 12,
                     dr:float = 0.02,
                     timestep:float = 0.1,
                     N_workers:int = 4):
    '''
    '''
    save_dir, N_frame, N_workers = sanity_check_multiple(trajectory, save_dir, target_atoms1, target_atoms2, N_workers)
    same = (target_atoms1 == target_atoms2)
    target_atoms1_index = np.array([atom.index for atom in trajectory[0] if atom.symbol==f'{target_atoms1}'])
    N_atom1 = len(target_atoms1_index)
    scale_traj1 = np.array([frame[target_atoms1_index].get_scaled_positions(wrap=False) for frame in trajectory])
    memmap_path1 = save_dir / f"temporary_info_for_vhfd_{target_atoms1}_{trajectory_tag}"
    memory_map(memmap_path1, scale_traj1)
    del scale_traj1
    if same:
        memmap_path2 = memmap_path1
        N_atom2 = N_atom1
    else:
        target_atoms2_index = np.array([atom.index for atom in trajectory[0] if atom.symbol==f'{target_atoms2}'])
        N_atom2 = len(target_atoms2_index)
        scale_traj2 = np.array([frame[target_atoms2_index].get_scaled_positions(wrap=False) for frame in trajectory])
        memmap_path2 = save_dir / f"temporary_info_for_vhfd_{target_atoms2}_{trajectory_tag}"
        memory_map(memmap_path2, scale_traj2)
        del scale_traj2
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
    lag_chunks = dynamic_chunks_create(N_frame, N_workers)
    def vhf_distinct_core(memmap_path1, memmap_path2, same, lag_list, N_frame, bins, histlength, r_max2, G):
        scale_traj1 = np.lib.format.open_memmap(memmap_path1, mode='r')
        scale_traj2 = np.lib.format.open_memmap(memmap_path2, mode='r')
        listlength = len(lag_list)
        partial_G_d = np.zeros([listlength, histlength])
        if same: 
            for lag_index, lag in enumerate(lag_list):
                n_slice = N_frame-lag
                slice_static = scale_traj1[:n_slice]
                slice_moving = scale_traj2[lag:]
                raw_rdf = np.zeros(histlength)
                for frame_index in range(n_slice):
                    pos1 = slice_static[frame_index] # shape (N_atoms, 3)
                    pos2 = slice_moving[frame_index]
                    diff = pos1[None, :, :] - pos2[:, None, :] # (N1, N2, 3)
                    diff -= np.round(diff)
                    r2 = np.einsum('...i,ij,...j->...', diff, G, diff, optimize='greedy') # dist_matrix = np.linalg.norm(diff @ cell, axis=-1)
                    np.fill_diagonal(r2, np.inf)
                    mask = r2 <= r_max2
                    r = np.sqrt(r2[mask])
                    raw_rdf += np.histogram(r, bins=bins)[0]
                partial_G_d[lag_index,:] = raw_rdf/n_slice # here is to take time-average, note that it isn't normalized yet!
        else:
            for lag_index, lag in enumerate(lag_list):
                n_slice = N_frame-lag
                slice_static = scale_traj1[:n_slice]
                slice_moving = scale_traj2[lag:]
                raw_rdf = np.zeros(histlength)
                for frame_index in range(n_slice):
                    pos1 = slice_static[frame_index] # shape (N_atoms, 3)
                    pos2 = slice_moving[frame_index]
                    diff = pos1[None, :, :] - pos2[:, None, :] # (N1, N2, 3)
                    diff -= np.round(diff)
                    r2 = np.einsum('...i,ij,...j->...', diff, G, diff, optimize='greedy') # dist_matrix = np.linalg.norm(diff @ cell, axis=-1)
                    mask = r2 <= r_max2
                    r = np.sqrt(r2[mask])
                    raw_rdf += np.histogram(r, bins=bins)[0]
                partial_G_d[lag_index,:] = raw_rdf/n_slice # here is to take time-average, note that it isn't normalized yet!
        del scale_traj1, scale_traj2
        return lag_list[0], partial_G_d
    results = Parallel(n_jobs=N_workers, backend="loky")(delayed(vhf_distinct_core)(memmap_path1, memmap_path2, same, lag_list, N_frame, bins, histlength, r_max2, G) for lag_list in lag_chunks)
    G_d = np.zeros([N_frame, histlength])
    for lag_start, partial_G_d in results:
        G_d[lag_start: lag_start + partial_G_d.shape[0]] = partial_G_d
    norm_factor = shell_vol * N_atom1 * N_atom2 / V
    normalized_G_d = G_d / norm_factor[None,:] # normalization
    dk = np.pi/r_max/10 # need to update
    k_space = np.arange(0, np.pi/dr/10, dk) # need to update
    isf = np.ones([N_frame, len(k_space)])
    for k in range(1,len(k_space)): # Fourier transformation to obtain static structure factors
        isf[:,k] = 1 + 4*np.pi*(N_atom1/V)* np.sum(distance * (normalized_G_d-1) * np.sin(k_space[k]*distance) / k_space[k] * dr, axis=1)
    h5f_path = save_dir / f"vhfd_{target_atoms1}_{target_atoms2}_{trajectory_tag}.hdf5"
    datasets = {"r_max": r_max,
                "dr": dr,
                "distance": distance,
                "V": V,
                "N_frame": N_frame,
                "timestep": timestep,
                "k_space": k_space,
                "N_atom1": N_atom1,
                "N_atom2": N_atom2,
                f"vhfd_{target_atoms1}_{target_atoms2}": normalized_G_d,
                f"isfd_{target_atoms1}_{target_atoms2}": isf}
    with h5py.File(h5f_path, "a") as h5f:
        for name, data in datasets.items():
            if name in h5f: del h5f[name]
            h5f.create_dataset(name, data=data)
    try:
        memmap_path1.unlink(missing_ok=True)
        if not same:
            memmap_path2.unlink(missing_ok=True)
    except OSError:
        pass




def vhf_self_cal(trajectory:List["ase.atoms.Atoms"],
                 trajectory_tag:str,
                 save_dir:str,
                 target_atoms:str,
                 r_max:float,
                 dr:float = 0.05,
                 timestep:float = 0.1,
                 N_workers:int = 4):
    '''
    '''
    save_dir, N_frame, N_workers = sanity_check(trajectory, save_dir, target_atoms, N_workers)
    target_atom_index = np.array([atom.index for atom in trajectory[0] if atom.symbol==f'{target_atoms}'])
    N_atom = len(target_atom_index)
    cell = np.array(trajectory[0].cell)
    a, b, c = trajectory[0].cell 
    bins = np.arange(0, r_max+dr, dr)
    histlength = len(bins)-1
    distance = np.linspace(0, r_max, histlength)
    shell_vol = (4/3)*np.pi*(bins[1:]**3 - bins[:-1]**3) # len = histlength
    V = trajectory[0].get_volume()
    traj = np.array([frame[target_atom_index].get_positions(wrap=False) for frame in trajectory])
    memmap_path = save_dir / f"temporary_info_for_vhfs_{target_atoms}_{trajectory_tag}"
    memory_map(memmap_path, traj)
    del traj
    lag_chunks = dynamic_chunks_create(N_frame, N_workers)
    def vhf_self_core(memmap_path, lag_list, N_frame, bins, histlength):
        traj = np.lib.format.open_memmap(memmap_path, mode='r')
        listlength = len(lag_list)
        partial_G_s = np.zeros([listlength, histlength])
        for index, lag in enumerate(lag_list):
            n_slice = N_frame-lag
            raw_rdf = np.zeros(histlength)
            block = max(1, min(4000, n_slice))
            for beg in range(0, n_slice, block):
                end = min(beg+block, n_slice)
                dis = np.linalg.norm(traj[beg+lag:end+lag] - traj[beg:end], axis=-1)
                raw_rdf += np.histogram(dis.ravel(), bins=bins)[0]
            partial_G_s[index, :] = raw_rdf/n_slice # here is to take time-average, note that it isn't normalized yet!
        del traj
        return lag_list[0], partial_G_s
    results = Parallel(n_jobs=N_workers, backend="loky")(delayed(vhf_self_core)(memmap_path, lag_list, N_frame, bins, histlength) for lag_list in lag_chunks)
    G_s = np.zeros([N_frame, histlength])
    for lag_start, partial_G_s in results:
        G_s[lag_start: lag_start + partial_G_s.shape[0]] = partial_G_s
    normalized_G_s = G_s / N_atom #(N_atom * shell_vol[None, :])
    dk = np.pi/r_max/10 # need to update
    k_space = np.arange(0, np.pi/dr/10, dk) # need to update
    isf = np.ones([N_frame, len(k_space)])
    for k in range(1,len(k_space)): # Fourier transformation to obtain static structure factors
        isf[:,k] = 4*np.pi*np.sum(distance * (normalized_G_s) * np.sin(k_space[k]*distance) / k_space[k] * dr, axis=1) # factor (N_atom/V)
    h5f_path = save_dir / f"vhfs_{target_atoms}_{trajectory_tag}.hdf5"
    datasets = {"r_max": r_max,
                "dr": dr,
                "distance": distance,
                "V": V,
                "shell_vol":shell_vol,
                "N_frame": N_frame,
                "timestep": timestep,
                "k_space": k_space,
                "N_atom": N_atom,
                f"vhfs_{target_atoms}": normalized_G_s,
                f"isfs_{target_atoms}": isf}
    with h5py.File(h5f_path, "a") as h5f:
        for name, data in datasets.items():
            if name in h5f: del h5f[name]
            h5f.create_dataset(name, data=data)
    try:
        memmap_path.unlink(missing_ok=True)
    except OSError:
        pass



def isf_tot_cal(trajectory:List["ase.atoms.Atoms"],
            trajectory_tag:str,
            save_dir:str,
            k0:float,
            dk_shell:float,
            timestep:float,
            target_atoms1:str,
            target_atoms2:str,
            N_workers:int = 4):
    '''
    '''
    save_dir, N_frame, N_workers = sanity_check_multiple(trajectory, save_dir, target_atoms1, target_atoms2, N_workers)
    same = (target_atoms1 == target_atoms2)
    target_atoms1_index = np.array([atom.index for atom in trajectory[0] if atom.symbol==f'{target_atoms1}'])
    N_atom1 = len(target_atoms1_index)
    traj1 = np.array([frame[target_atoms1_index].get_positions(wrap=True) for frame in trajectory])
    memmap_path1 = save_dir / f"temporary_info_for_isftot_{target_atoms1}_{trajectory_tag}"
    memory_map(memmap_path1, traj1)
    del traj1
    if same:
        memmap_path2 = memmap_path1
        N_atom2 = N_atom1
    else:
        target_atoms2_index = np.array([atom.index for atom in trajectory[0] if atom.symbol==f'{target_atoms2}'])
        N_atom2 = len(target_atoms2_index)
        traj2 = np.array([frame[target_atoms2_index].get_positions(wrap=True) for frame in trajectory])
        memmap_path2 = save_dir / f"temporary_info_for_isftot_{target_atoms2}_{trajectory_tag}"
        memory_map(memmap_path2, traj2)
        del traj2
    V = trajectory[0].get_volume()
    a, b, c = trajectory[0].cell 
    b1 = 2 * np.pi * np.cross(b, c) / V  # reciprocal basis
    b2 = 2 * np.pi * np.cross(c, a) / V
    b3 = 2 * np.pi * np.cross(a, b) / V
    B = np.vstack([b1, b2, b3])          # B = (3,3) reciprocal basis
    hmax = int(np.ceil(k0 / np.linalg.norm(b1)))
    kmax = int(np.ceil(k0 / np.linalg.norm(b2)))
    lmax = int(np.ceil(k0 / np.linalg.norm(b3)))       
    grid = np.array(np.meshgrid(np.arange(-hmax, hmax+1), np.arange(-kmax, kmax+1), np.arange(-lmax, lmax+1), indexing='ij')).reshape(3,-1).T 
    k_vec_raw = grid @ B
    k_mod_raw = np.linalg.norm(k_vec_raw, axis=1)   # (N_k,)
    mask = np.abs(k_mod_raw - k0) <= dk_shell/2
    k_vec = k_vec_raw[mask]  # (N_k,3)
    N_k = k_vec.shape[0]
    if N_k == 0:
        raise RuntimeError(f"No k-vectors found in [{k0-dk_shell/2:.3f}, {k0+dk_shell/2:.3f}]")
    normalization  = N_atom1**2 if same else N_atom1*N_atom2
    lag_chunks = dynamic_chunks_create(N_frame, N_workers)
    def isf_tot_core(memmap_path1, memmap_path2, lag_list, normalization, N_frame, k_vec, N_k):
        traj1 = np.lib.format.open_memmap(memmap_path1, mode='r') # (N_frame, N_atom1, 3)
        traj2 = np.lib.format.open_memmap(memmap_path2, mode='r')
        partial_F_tot = np.zeros((len(lag_list),), dtype=np.complex128)
        for index, lag in enumerate(lag_list):
            n_slice = N_frame - lag
            accum = np.zeros(N_k, dtype=np.complex128)
            lag_block = max(1, min(128, n_slice))
            for start in range(0, n_slice, lag_block):
                end = min(start+lag_block, n_slice)
                pos_a = traj1[start : end]
                pos_b = traj2[start+lag : end+lag]
                phase1 = np.tensordot(k_vec, pos_a, axes=([1],[2]))  # (k_batch, lag_block, N_atom1)
                phase2 = np.tensordot(k_vec, pos_b, axes=([1],[2]))  # (k_batch, lag_block, N_atom2)
                rho1 = np.exp(+1j*phase1).sum(axis=2)
                rho2 = np.exp(+1j*phase2).sum(axis=2)
                accum += np.sum(rho1.conj() * rho2, axis=1)
            partial_F_tot[index] =  accum.sum() / (n_slice*normalization*N_k)
        del traj1, traj2
        return lag_list[0], partial_F_tot
    results = Parallel(n_jobs=N_workers, backend="loky")(delayed(isf_tot_core)(memmap_path1, memmap_path2, lag_list, normalization, N_frame, k_vec, N_k) for lag_list in lag_chunks)
    F_tot = np.zeros(N_frame, dtype=np.complex128)
    for lag_start, partial_F_tot in results:
        F_tot[lag_start: lag_start + partial_F_tot.shape[0]] = partial_F_tot
    h5f_path = save_dir / f"isf_{target_atoms1}_{target_atoms2}_{trajectory_tag}.hdf5"
    datasets = {"reciprocal_basis": B,
                "volume": V,
                "N_frame": N_frame,
                "timestep": timestep,
                "N_atom1": N_atom1,
                "N_atom2": N_atom2,
                "k_vec": k_vec,
                "k0": k0,
                f"isf_{target_atoms1}_{target_atoms2}": F_tot}
    with h5py.File(h5f_path, "a") as h5f:
        for name, data in datasets.items():
            if name in h5f: del h5f[name]
            h5f.create_dataset(name, data=data)
    try:
        memmap_path1.unlink(missing_ok=True)
        if not same:
            memmap_path2.unlink(missing_ok=True)
    except OSError:
        pass



def isf_self_cal(trajectory:List["ase.atoms.Atoms"],
            trajectory_tag:str,
            save_dir:str,
            k0:float,
            dk_shell:float,
            timestep:float,
            target_atoms:str,
            N_workers:int = 4):
    '''
    '''
    save_dir, N_frame, N_workers = sanity_check(trajectory, save_dir, target_atoms, N_workers)
    target_atoms_index = np.array([atom.index for atom in trajectory[0] if atom.symbol==f'{target_atoms}'])
    N_atom = len(target_atoms_index)
    traj = np.array([frame[target_atoms_index].get_positions(wrap=False) for frame in trajectory])
    memmap_path = save_dir / f"temporary_info_for_isfself_{target_atoms}_{trajectory_tag}"
    memory_map(memmap_path, traj)
    del traj
    V = trajectory[0].get_volume()
    a, b, c = trajectory[0].cell 
    b1 = 2 * np.pi * np.cross(b, c) / V  # reciprocal basis
    b2 = 2 * np.pi * np.cross(c, a) / V
    b3 = 2 * np.pi * np.cross(a, b) / V
    B = np.vstack([b1, b2, b3])          # B = (3,3) reciprocal basis
    hmax = int(np.ceil(k0 / np.linalg.norm(b1)))
    kmax = int(np.ceil(k0 / np.linalg.norm(b2)))
    lmax = int(np.ceil(k0 / np.linalg.norm(b3)))       
    grid = np.array(np.meshgrid(np.arange(-hmax, hmax+1), np.arange(-kmax, kmax+1), np.arange(-lmax, lmax+1), indexing='ij')).reshape(3,-1).T 
    k_vec_raw = grid @ B
    k_mod_raw = np.linalg.norm(k_vec_raw, axis=1)   # (N_k,)
    mask = np.abs(k_mod_raw - k0) <= dk_shell/2
    k_vec = k_vec_raw[mask]  # (N_k,3)
    N_k = k_vec.shape[0]
    if N_k == 0:
        raise RuntimeError(f"No k-vectors found in [{k0-dk_shell/2:.3f}, {k0+dk_shell/2:.3f}]")
    lag_chunks = dynamic_chunks_create(N_frame, N_workers)
    def isf_self_core(memmap_path, lag_list, N_atom, N_frame, k_vec, N_k):
        traj = np.lib.format.open_memmap(memmap_path, mode='r') # (N_frame, N_atom, 3)
        partial_F_s = np.zeros((len(lag_list),), dtype=np.complex128)
        for index, lag in enumerate(lag_list):
            n_slice = N_frame - lag
            accum = 0+0j
            lag_block = max(1, min(128, n_slice))
            for start in range(0, n_slice, lag_block):
                end = min(start+lag_block, n_slice)
                pos_a = traj[start : end]
                pos_b = traj[start+lag : end+lag]
                diff = pos_b - pos_a
                phase = np.tensordot(k_vec, diff, axes=([1],[2]))  # (N_k, lag_block, N_atom)
                rho   = np.exp(-1j*phase).sum(axis=2)  # (N_k, block)
                accum += rho.sum()
            partial_F_s[index] =  accum / (n_slice*N_atom*N_k)
        del traj
        return lag_list[0], partial_F_s
    results = Parallel(n_jobs=N_workers, backend="loky")(delayed(isf_self_core)(memmap_path, lag_list, N_atom, N_frame, k_vec, N_k) for lag_list in lag_chunks)
    F_s = np.zeros(N_frame, dtype=np.complex128)
    for lag_start, partial_F_s in results:
        F_s[lag_start: lag_start + partial_F_s.shape[0]] = partial_F_s
    h5f_path = save_dir / f"isf_{target_atoms}_{trajectory_tag}.hdf5"
    datasets = {"reciprocal_basis": B,
                "volume": V,
                "N_frame": N_frame,
                "timestep": timestep,
                "N_atom": N_atom,
                "k_vec": k_vec,
                "k0": k0,
                f"isf_{target_atoms}": F_s}
    with h5py.File(h5f_path, "a") as h5f:
        for name, data in datasets.items():
            if name in h5f: del h5f[name]
            h5f.create_dataset(name, data=data)
    try:
        memmap_path.unlink(missing_ok=True)
    except OSError:
        pass

