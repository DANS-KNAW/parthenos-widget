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
    policyfield = majorkey
    try:
        df = df[pd.notnull(df[majorkey])]
    except:
	df = df[pd.notnull(df[policykey])]
	policyfield = policykey
    major = {}
    for polname in df[policyfield]:
        polline = df[df[policyfield] == polname][location]
        locname = polline.iloc[0]
        if locname:
            major[polname] = str(locname)
    data = {}
    data['data'] = major
    datajson = json.dumps(data, ensure_ascii=True, sort_keys=True, indent=4)
    return datajson

# Filter on FAIR principles
def fair(tabname):
    df = pd.read_excel(MATRIX, tabname, header=1, skiprows=0)
    fairfilter = {}
    for column in df.columns:
        if re.search("FINDABLE", column, re.DOTALL): #, re.MULTILINE):
            fairfilter['FINDABLE'] = column
        if re.search("ACCESSIBLE", column, re.DOTALL): #, re.MULTILINE):
            fairfilter['ACCESSIBLE'] = column
        if re.search("INTEROPERABLE", column, re.DOTALL): #, re.MULTILINE):
            fairfilter['INTEROPERABLE'] = column
        if re.search("REUSABLE", column, re.DOTALL): #, re.MULTILINE):
            fairfilter['REUSABLE'] = column
    return (df, fairfilter)
