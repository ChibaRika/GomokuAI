from distutils.core import setup
from Cython.Build import cythonize

setup(
    name="gomoku",
    ext_modules=cythonize("gomoku.pyx")
)
