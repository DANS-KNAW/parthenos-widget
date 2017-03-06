#!/usr/bin/python
from __future__ import print_function, absolute_import

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
#import pytest
from tests.config import MATRIX
from parthenos.core.datatojson import *
import uuid
import httpretty
import requests
import pandas as pd
import simplejson
import json

if __name__ == '__main__':
    print ('%s' % policies(4))
    (df, fairtest) = fair(4) 
    print ('%s' % fairtest)
    x = fairfilter(df, fairtest, 'fair')
    print ('%s' % x.to_html())
