from setuptools import setup, find_packages, Extension
import numpy
from Cython.Build import cythonize
from pathlib import Path

#dir = Path(__file__).parent
#long_description = (dir / "README.md").read_text()

setup(
    ext_modules = cythonize(Extension('dtw_flex.core_cython.dtw_cy',
        ["dtw_flex/core_cython/dtw_cy.pyx"],
        include_dirs=[numpy.get_include()])),

)