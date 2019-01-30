#!/usr/bin/python

import re
import sys
import pandas as pd
import numpy as np
import json
from parthenos.settings import *

def filtertodict(params):
    keys = {}
    for thisstr in params:
        info = re.match(r'(\S+)\:(.+)$', thisstr)
        if info:
            keys[info.group(2)] = info.group(1)
    return keys

def mainfilter(df, params):
    alltopics = {}
    data = ''
    discipline = ''
    selection = ['policy','policy link', 'organisation']

    # Filtering data
    matrix = []
    selected = []
    skip = 0
    for name in params:
        if params[name] == 'topic':
            try:
                matrix.append(df[name]=='X')
                selected.append(name)
                selection.append(name)
            except:
                skip = 1

    if matrix:
        fmatrix = matrix[0]
        for i in range(1, len(matrix)):
            fmatrix = (fmatrix) | (matrix[i])
        data = df[fmatrix]

    # Final result
    result = {}
    data = data.replace(np.nan, '', regex=True)
    ymatrix = data[selection]

    topic2fair = {}
    for col in selected:
	topic2fair[col] = df.ix[0][col]
        rowarray = []
        for row in ymatrix.index:
            rowresult = {}
	    rowsubset = ymatrix.ix[row]
            if rowsubset[col] == 'X':
                d = rowsubset.to_dict() #orient='records')
                rowarray.append(d)
        result[col] = rowarray

    return (result, topic2fair)

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

# "community:RESEARCH COMMUNITY",discipline:SOCIAL SCIENCE","topic:REUSABLE (provenance; usage licence; standards)"
def filtertodict(params):
    keys = {}
    for thisstr in params:
	info = re.match(r'(\S+)\:(.+)$', thisstr)
	if info:
    	    keys[info.group(2)] = info.group(1)
    return keys

def gettopics(tabname):
    alltopics = {}
    xl = pd.ExcelFile(MATRIX)
    df = pd.read_excel(MATRIX, sheetname=tabname, skiprows=1)
    columns = []
    for colname in df.columns:
        if colname not in forbidden:
            columns.append(colname)
    alltopics['topics'] = columns
    cdata = json.dumps(alltopics, ensure_ascii=False, sort_keys=True, indent=4)
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

def frametokeys(df):
    allkeys = {}
    for item in df.columns:
        allkeys[item] = ''
    return allkeys

def frametovalues(df):
    allvalues = {}
    skip = 0
    for thisindex in df.index:
        line = df.ix[thisindex]
        for col in line:
            try:
                allvalues[str(col)] = ''
            except:
                skip = 1
                
        finalvalues = []
        for item in sorted(allvalues):
            finalvalues.append(item)
    return finalvalues

# Filtering out policies based on FAIR acronyms
def fairfilter(df, filters, command):
    fairmatrix = {}
    fairmatrix['f'] = df[filters['FINDABLE']]=='X'
    fairmatrix['a'] = df[filters['ACCESSIBLE']]=='X'
    fairmatrix['i'] = df[filters['INTEROPERABLE']]=='X'
    fairmatrix['r'] = df[filters['REUSABLE']]=='X'

    resultmatrix = pd.DataFrame()
    for acr in command:
        if resultmatrix.empty:   
            resultmatrix = fairmatrix[acr]
        else:
            resultmatrix = resultmatrix & fairmatrix[acr]
            
    return df[resultmatrix]
