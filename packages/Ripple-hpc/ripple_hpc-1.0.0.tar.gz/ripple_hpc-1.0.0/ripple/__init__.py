"""
CorrelationAnalysis
==========

This is a brief but efficient package that uses only trajectory information to quantify the correlation of particles in stochastic motion.


Documentation: 

When using tidynamics in a publication, please cite the following paper:



"""
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

from .static import sanity_check_multiple, chunks_create_for_rdf, chunks_create_for_ssf, memory_map_multiple, rdf_cal, rdf_core, ssf_cal, ssf_core
from .dynamic import sanity_check, dynamic_chunks_create, memory_map_single, msd_cal, msd_core, cmsd_cal, cmsd_core, cross_corre_cal, cross_corre_core
from .correlation import vhf_self_cal, vhf_self_core, vhf_distinct_cal, vhf_distinct_core, isf_self_cal, isf_self_core, isf_distinct_cal, isf_distinct_core


with open(os.path.join(os.path.dirname(__file__), 'VERSION')) as f:
    __version__ = f.read().strip()