# Available at setup time due to pyproject.toml
import glob
import os

from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import find_packages, setup

__version__ = "2.0.0"

EIGEN_INCLUDE_DIR = os.path.abspath("/opt/homebrew/Cellar/eigen/3.4.1/include/eigen3")

ext_modules = [
    Pybind11Extension(
        "_mqds",
        glob.glob("mqds/mqds_lib/*.cpp"),
        include_dirs=[EIGEN_INCLUDE_DIR],
        define_macros=[("VERSION_INFO", __version__)],
    ),
]

setup(
    name="mqds",
    packages=find_packages(),
    version=__version__,
    author="Justin Provazza",
    author_email="jprov410@gmail.com",
    url="https://github.com/jprovazza/mqds",
    description="Molecular Quantum Dynamics and Spectroscopy.",
    long_description="",
    ext_modules=ext_modules,
    extras_require={"test": "pytest"},
    # Currently, build_ext only provides an optional "highest supported C++
    # level" feature, but in the future it may provide more features.
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.11",
)
