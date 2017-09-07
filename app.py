from __future__ import print_function, absolute_import

import sys
import os
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from flask import Flask, redirect, make_response, Response, render_template, request, send_from_directory
#from tests.config import MATRIX
#from parthenos.core.datatojson import *
import uuid
import httpretty
import requests
import pandas as pd
import simplejson
import json
app = Flask(__name__)

basedir = "%s" % os.getenv("HOME")
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

def dataloader(topickey):
    df = pd.read_hdf("%s/%s.h5" % (cachedir, topickey), 'key')
    return df

def contents(tabname):
    data = read_contents("CONTENTS")
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
    return Response(cdata,  mimetype='application/json')

def list():
    data = read_contents("CONTENTS")
    tablist = {}
    tabs = []
    for name in data['name']:
        tabs.append(name)
    tablist['data'] = tabs
    data = json.dumps(tablist, ensure_ascii=False, sort_keys=True, indent=4)
    return Response(data,  mimetype='application/json')

def gettopics(tabname):
    alltopics = {}
    topickey = "SOCIAL SCIENCE"
    if tabname:
	topickey = tabname 
    df = dataloader(topickey)
    columns = []
    for colname in df.columns:
        if colname not in forbidden:
            columns.append(colname)
    alltopics['topics'] = columns
    cdata = json.dumps(alltopics, ensure_ascii=False, sort_keys=True, indent=4)
    return cdata

def datacache(cachedir):
    xl = pd.ExcelFile(MATRIX)
    for tabname in xl.sheet_names:
        if tabname == 'CONTENTS':
            df = pd.read_excel(MATRIX, sheetname=tabname, header=None, skiprows=0)
        else:
            df = pd.read_excel(MATRIX, sheetname=tabname, header=1, skiprows=0)
        df.to_hdf("%s/%s.h5" % (cachedir, str(tabname)), 'key', data_columns=True)
    return 'done'

def read_contents(tabname):
    wizardkey = 'Navigation'
    df = dataloader(tabname)
    df = df[df[2] == wizardkey]
    df.columns = ('name', 'community', 'type')
    df = df.drop('type', 1)
    return df

@app.route("/")
def main():
    return 'Wizard is running...'

@app.route("/webfilter", methods=['GET', 'POST'])
def webfilter():
    newfilterparams = []
    try:
         qinput = json.loads( request.data )
         for name in qinput.keys():
             newfilterparams.append(str(name))
    except:
	return 'no data'

    #newfilterparams = ["community:RESEARCH COMMUNITY","discipline:SOCIAL SCIENCE","topic:CITATION GUIDELINES", "topic:PRIVACY AND SENSITIVE DATA"]
    params = filtertodict(newfilterparams)
    discipline = ''
    for name in params:
        if params[name] == 'discipline':
            discipline = name
	    df = dataloader(discipline)
    if discipline == '':
        for name in params: 
            if params[name] == 'community':
                discipline = name
		df = dataloader(discipline)

    outmatrix = mainfilter(df, filtertodict(newfilterparams))
    data = json.dumps(outmatrix, ensure_ascii=False, sort_keys=True, indent=4)
    return Response(data,  mimetype='application/json')

@app.route("/contents")
def webcontents():
    return contents('CONTENTS')

@app.route("/list")
def showlist():
    return list()

@app.route("/topics", methods=['GET', 'POST'])
def webtopics():
    maindiscipline = 'SOCIAL SCIENCE'
    if request.data:
        qinput = json.loads( request.data )
        thistopic = ''
        for name in qinput:
            m = re.match(r'discipline\:(.+)$', name)
            if m:
                thistopic = m.group(1)
        if thistopic:
            maindiscipline = thistopic
        else:
            m = re.match(r'community\:(.+)$', name)
            if m:
                maindiscipline = m.group(1)
    maindiscipline = 'ARCHAEOLOGY'
    return gettopics(maindiscipline)

if __name__ == '__main__':
    s = datacache(cachedir)
    app.run(host='0.0.0.0', port=8081)
