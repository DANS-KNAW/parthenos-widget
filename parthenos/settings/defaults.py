from __future__ import absolute_import

import os

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.abspath(os.path.join(HERE, os.pardir))

matrixfile = "matrix20170515.xlsx"
MATRIX = os.path.join(BASE_PATH, '../data', matrixfile)
forbidden = ['POLICY', 'POLICY LINK', 'COUNTRY', 'ORGANISATION', 'ORGANISATION LINK', 'PROJECT']
majorkey = "POLICY"
policykey = "FORMAL POLICY"
location = 'COUNTRY'
