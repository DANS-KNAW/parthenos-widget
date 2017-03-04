#!/usr/bin/python

import re
import sys
import pandas as pd
import numpy as np
import json
from parthenos.settings import *

def contents(tabname):
    df = pd.read_excel(MATRIX, sheetname=tabname, header=None, skiprows=0)
    data = df #.transpose()
    content = {}
    for index in data.index:
        row = data.ix[index]
        if str(row[1]) != 'nan':
            content[row[0]] = row[1]
        else:
            content[row[0]] = ''
    data = {}
    data['contents'] = content
    cdata = json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4)
    return cdata
   
def policies(tabname):
    df = pd.read_excel(MATRIX, sheetname=tabname, header=1, skiprows=0)
    df = df[pd.notnull(df[majorkey])]
    major = {}
    for polname in df[majorkey]:
        polline = df[df[majorkey] == polname][location]
        locname = polline.iloc[0]
        if locname:
            major[polname] = str(locname)
    data = {}
    data['data'] = major
    datajson = json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4)
    return datajson
