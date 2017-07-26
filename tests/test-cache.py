from __future__ import print_function, absolute_import

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
#from tests.config import MATRIX
#from parthenos.core.datatojson import *
import uuid
import httpretty
import requests
import pandas as pd
import simplejson
import json

basedir = os.path.dirname(os.path.realpath(__file__))
datadir = "%s/../data" % basedir
cachedir = "%s/../%s" % (basedir, "cache")

sys.path.append(basedir)
from parthenos.core.datatojson import *
from parthenos.settings import *
import tables
from pandas import HDFStore

def dataloader(topickey):
    df = pd.read_hdf("%s/%s.h5" % (cachedir, topickey), 'key')
    return df

def read_contents(tabname):
    wizardkey = 'Navigation'
    df = dataloader(tabname)
    df = df[df[2] == wizardkey]
    df.columns = ('name', 'community', 'type')
    df = df.drop('type', 1)
    return df

#topickey = "CONTENTS"
#x = read_contents("CONTENTS")

topickey = "SOCIAL SCIENCE"
df = dataloader(topickey)
print ("%s" % df.to_html())

