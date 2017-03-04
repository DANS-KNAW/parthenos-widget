from __future__ import absolute_import
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from parthenos.settings import BASE_PATH

MATRIX = os.path.join(BASE_PATH, '../data', 'matrixc.xlsx')

EXAMPLE_FILES = [
    os.path.join(BASE_PATH, 'tests', '__init__.py'),
    os.path.join(BASE_PATH, 'tests', 'config.py'),
]
print MATRIX
