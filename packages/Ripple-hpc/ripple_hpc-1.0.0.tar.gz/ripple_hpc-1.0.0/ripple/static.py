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

def chunks_create_for_rdf(N_frame, N_workers):
    if N_workers == 1:
        return [np.arange(N_frame)]
    else:
        return np.array_split(np.arange(N_frame), N_workers)

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

def rdf_cal(trajectory:List["ase.atoms.Atoms"],
            trajectory_tag:str,
            save_dir:str,
            target_atoms1:str,
            target_atoms2:str,
            r_max:float = 12,
            dr:float = 0.02,
            N_workers:int = 4):
    '''
    '''
    save_dir, N_frame, N_workers = sanity_check_multiple(trajectory, save_dir, target_atoms1, target_atoms2, N_workers)
    same = (target_atoms1 == target_atoms2)
    target_atoms1_index = np.array([atom.index for atom in trajectory[0] if atom.symbol==f'{target_atoms1}'])
    N_atom1 = len(target_atoms1_index)
    scale_traj1 = np.array([frame[target_atoms1_index].get_scaled_positions(wrap=False) for frame in trajectory])
    memmap_path1 = save_dir / f"temporary_info_for_rdf_{target_atoms1}_{trajectory_tag}"
    memory_map(memmap_path1, scale_traj1)
    del scale_traj1
    if same:
        memmap_path2 = memmap_path1
        N_atom2 = N_atom1
    else:
        target_atoms2_index = np.array([atom.index for atom in trajectory[0] if atom.symbol==f'{target_atoms2}'])
        N_atom2 = len(target_atoms2_index)
        scale_traj2 = np.array([frame[target_atoms2_index].get_scaled_positions(wrap=False) for frame in trajectory])
        memmap_path2 = save_dir / f"temporary_info_for_rdf_{target_atoms2}_{trajectory_tag}"
        memory_map(memmap_path2, scale_traj2)
        del scale_traj2
    cell = np.array(trajectory[0].cell)
    G = cell @ cell.T 
    a, b, c = trajectory[0].cell 
    r_max = min(r_max, np.linalg.norm(np.dot(a, np.cross(b,c)))*0.5/max(np.linalg.norm(np.cross(a,b)), np.linalg.norm(np.cross(b,c)), np.linalg.norm(np.cross(c,a))))
    bins = np.arange(0, r_max+dr, dr)
    histlength = len(bins)-1
    distance = np.linspace(0, r_max, histlength)  #0.5*(bins[1:]+bins[:-1])
    shell_vol = (4/3)*np.pi*(bins[1:]**3 - bins[:-1]**3) # shell_vol.size = histlength
    V = trajectory[0].get_volume()
    lag_chunks = chunks_create_for_rdf(N_frame, N_workers)
    def rdf_core(memmap_path1, memmap_path2, same, lag_list, bins, histlength, G):
        scale_traj1 = np.lib.format.open_memmap(memmap_path1, mode='r')[lag_list]
        scale_traj2 = np.lib.format.open_memmap(memmap_path2, mode='r')[lag_list]
        listlength = len(lag_list) # the length of the lag time in one chunk, only determine the scale of matrix
        partial_rdf = np.zeros(histlength)
        lag_block = 128
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
            for s in range(0, listlength, lag_block):
                pos1 = scale_traj1[s:s+lag_block]
                pos2 = scale_traj2[s:s+lag_block]
                diff = pos1[:, None, :, :] - pos2[:, :, None, :]  # shape: (lag_block, N_target1, N_target2, 3)
                diff -= np.round(diff)
                r2 = np.einsum('...i,ij,...j->...', diff, G, diff, optimize='greedy')
                r = np.sqrt(r2, out=r2).ravel()
                partial_rdf += np.histogram(r, bins=bins)[0]
        del scale_traj1, scale_traj2
        return partial_rdf
    results = Parallel(n_jobs=N_workers, backend="loky")(delayed(rdf_core)(memmap_path1, memmap_path2, same, lag_list, bins, histlength, G) for lag_list in lag_chunks)
    rdf = np.zeros(histlength)
    for partial_rdf in results:
        rdf += partial_rdf
    total_rdf = rdf / N_frame
    total_rdf = total_rdf/(shell_vol * N_atom1 * N_atom2 / V) # normalization
    dk = np.pi/r_max/10                     # need to update
    k_space = np.arange(0, np.pi/dr/10, dk) # need to update
    total_ssf = np.zeros(len(k_space))
    for k in range(1,len(k_space)): # Fourier transformation to obtain static structure factors
        total_ssf[k] = 1 + 4*np.pi*(N_atom2/V)* np.sum(distance * (total_rdf-1) * np.sin(k_space[k]*distance) / k_space[k] * dr, axis=0)
    h5f_path = save_dir / f"rdf_{target_atoms1}_{target_atoms2}_{trajectory_tag}.hdf5"
    datasets = {"distance": distance,
                "k_space": k_space,
                "volume": V,
                "N_atom1": N_atom1,
                "N_atom2": N_atom2,
                f"RDF_{target_atoms1}_{target_atoms2}": total_rdf,
                f"SSF_{target_atoms1}_{target_atoms2}": total_ssf}
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




def ssf_cal(trajectory:List["ase.atoms.Atoms"],
            trajectory_tag:str,
            save_dir:str,
            k_max:float,
            dk_shell:float,
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
    memmap_path1 = save_dir / f"temporary_info_for_ssf_{target_atoms1}_{trajectory_tag}"
    memory_map(memmap_path1, traj1)
    del traj1
    if same:
        memmap_path2 = memmap_path1
        N_atom2 = N_atom1
    else:
        target_atoms2_index = np.array([atom.index for atom in trajectory[0] if atom.symbol==f'{target_atoms2}'])
        N_atom2 = len(target_atoms2_index)
        traj2 = np.array([frame[target_atoms2_index].get_positions(wrap=True) for frame in trajectory])
        memmap_path2 = save_dir / f"temporary_info_for_ssf_{target_atoms2}_{trajectory_tag}"
        memory_map(memmap_path2, traj2)
        del traj2
    normalization  = np.sqrt(N_atom1*N_atom2)
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
    def ssf_core(memmap_path1, memmap_path2, lag_list, same, normalization, k_vec):
        pos_a = np.lib.format.open_memmap(memmap_path1, mode='r')[lag_list] # (N_lag, N_atom1, 3)
        pos_b = np.lib.format.open_memmap(memmap_path2, mode='r')[lag_list]
        Nk = len(k_vec)
        Sab_k  = np.zeros(Nk)
        k_batch = 2048
        for s in range(0, Nk, k_batch):
            end = min(s+k_batch, Nk)
            k_b = k_vec[s:end]  # k_b is k_batch, batch length is b
            phase_a = np.tensordot(k_b, pos_a, axes=([1], [2])) # (k_b.shape[0], N_lag, N_atom1)
            rho_a = np.exp(1j * phase_a).sum(axis=2) # (b, N_lag)
            if same:
                Sab_frame = (rho_a.conj() * rho_a).real / normalization # (C_a**2 + S_a**2) / sqrtN
            else:
                phase_b = np.tensordot(k_b, pos_b, axes=([1],[2]))
                rho_b   = np.exp(1j * phase_b).sum(axis=2)
                Sab_frame = (rho_a.conj() * rho_b).real / normalization # (C_a*C_b + S_a*S_b) / sqrtN
            Sab_k[s:end] = Sab_frame.sum(axis=1)        # sum over N_lag then take average outside
        del pos_a, pos_b
        return Sab_k
    lag_chunks = chunks_create_for_ssf(N_frame, N_workers)
    results = Parallel(n_jobs=N_workers, backend="loky")(delayed(ssf_core)(memmap_path1, memmap_path2, lag_list, same, normalization, k_vec) for lag_list in lag_chunks)
    ssf = np.zeros(len(k_vec))
    for partial_ssf in results:
        ssf = ssf + partial_ssf
    ssf = ssf / N_frame
    ssf_shell = np.bincount(shell, weights=ssf, minlength=Nshell)
    cnt_shell = np.bincount(shell, minlength=Nshell)
    ssf_shell /= np.maximum(cnt_shell, 1)
    h5f_path = save_dir / f"ssf_{target_atoms1}_{target_atoms2}_{trajectory_tag}.hdf5"
    datasets = {"reciprocal_basis": B,
                "k_space": k_mid,
                "volume": V,
                "N_atom1": N_atom1,
                "N_atom2": N_atom2,
                f"SSF_{target_atoms1}_{target_atoms2}": ssf_shell}
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

