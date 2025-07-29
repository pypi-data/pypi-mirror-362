
from setuptools import Extension, setup
import os

if __name__ == '__main__':
    setup(
        build_golang={'root': 'github.com/MikeMoore63/pyrustaudit'},
        ext_modules=[Extension('pyrustaudit._pyrustaudit', ['src/pyrustaudit/pyrustaudit.go'])]
    )
