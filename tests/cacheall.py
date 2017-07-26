from __future__ import print_function, absolute_import

import sys
import os
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
#from tests.config import MATRIX
#from parthenos.core.datatojson import *
import uuid
import httpretty
import requests
import pandas as pd
import simplejson
import json

basedir = "%s/%s" % (os.getenv("HOME"), "projects/parthenos-widget")
datadir = "%s/data" % basedir
cachedir = "%s/%s" % (basedir, "cache")
sys.path.append(basedir)
#from tests.config import MATRIX
from parthenos.core.datatojson import *
from parthenos.settings import *
import tables
from pandas import HDFStore
try:
    os.stat(cachedir)
except:
    os.mkdir(cachedir)

def datacache(cachedir):
    xl = pd.ExcelFile(MATRIX)
    for tabname in xl.sheet_names:
        if tabname == 'CONTENTS':
            df = pd.read_excel(MATRIX, sheetname=tabname, header=None, skiprows=0)
        else:
            df = pd.read_excel(MATRIX, sheetname=tabname, header=1, skiprows=0)
        df.to_hdf("%s/%s.h5" % (cachedir, str(tabname)), 'key', data_columns=True)
    return 'done'
s = datacache(cachedir)
