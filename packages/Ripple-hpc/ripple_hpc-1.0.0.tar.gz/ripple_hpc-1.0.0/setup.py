from setuptools import setup, find_packages
import io
import os

# read README.md
here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# read ripple/VERSION
with open(os.path.join(here, "ripple", "VERSION")) as f:
    version = f.read().strip()

# acclaim 
setup(
    name="Ripple-hpc",
    version=version,
    author="LuciusLiu",
    author_email="l.liu21@imperial.ac.uk",
    description="Ripple is a Python package designed to analyze particle-motion correlation functions at scale. By leveraging multicore parallelism, Ripple efficiently computes correlation functions for very large trajectory datasets. Trajectories are ingested via ASE, ensuring compatibility with virtually any supported file format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/orgs/Frost-group/repositories/Ripple",
    packages=find_packages(exclude=["tests*", "docs*"]),
    install_requires=[
        "numpy",
        "ase",
        "h5py",
        "joblib",
        "psutil",        
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)