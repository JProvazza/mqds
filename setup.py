# Available at setup time due to pyproject.toml
import glob

from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import find_packages, setup

__version__ = "2.0.0"

ext_modules = [
    Pybind11Extension(
        "_mqds",
        glob.glob("mqds/lib/*.cpp"),
        # Example: passing in the version to the compiled code
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
