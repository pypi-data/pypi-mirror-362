
from setuptools import Extension, setup
import os

if __name__ == '__main__':
    setup(
        build_golang={'root': 'github.com/MikeMoore63/pyrpmdb'},
        ext_modules=[Extension('pyrpmdb._pyrpmdb', ['src/pyrpmdb/pyrpmdb.go'])]
    )
