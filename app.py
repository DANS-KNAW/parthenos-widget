from __future__ import print_function, absolute_import

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
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

def frametoxml(df):
    allvalues = {}
    skip = 0
    tmpxml = ""
    for thisindex in df.index:
        line = df.ix[thisindex]
        #print str(line)
        tmpxml = tmpxml + "\n\t<item id=\"%s\">" % str(thisindex)
        for col in df.columns:
            #print "\t%s %s" % (col, str(thisindex))
            colname = col
            colname = colname.replace("\n", '_', 10)
            colname = colname.replace('&', '&amp;', 30)
            value = str(df.ix[thisindex][col])
            value = value.replace('&','&amp;').decode('utf-8')
            if value == 'nan':
                value = ''
            else:
                tmpxml = tmpxml + "\n\t\t<column name=\"%s\">%s</column>" % (colname, value)
            #print col
            try:
                allvalues[str(col)] = ''
            except:
                skip = 1
        tmpxml = tmpxml + "\n</item>"
                
        finalvalues = []
        for item in sorted(allvalues):
            finalvalues.append(item)
    return tmpxml

def matrix2xml():
    sheetid = 0
    xmlcontent = "<?xml version=\"1.0\"?>"
    xmlcontent = xmlcontent + "\n<data>"
    data = read_contents("CONTENTS")
    content = {}
    for index in data.index:
        row = data.ix[index]
        if str(row[1]) != 'nan':
            content[row[0]] = row[1]
        else:
            content[row[0]] = ''

    for dname in content:
	df = dataloader(dname)
        if sheetid:
            xmlcontent = xmlcontent + "\n\t<discipline name=\"%s\" >" % dname
            tmpxml = frametoxml(df)
            xmlcontent =  xmlcontent + tmpxml + "\n</discipline>"
        sheetid = sheetid + 1
    xmlcontent = xmlcontent + "\n</data>"
    return xmlcontent

def dataloader(topickey):
    df = pd.read_hdf("%s/%s.h5" % (cachedir, topickey), 'key')
    return df

def getprinciples(tabname):
    xl = pd.ExcelFile(MATRIX)
    df = pd.read_excel(MATRIX, sheetname=tabname, header=0, skiprows=0)
    
    principles = []
    for i in df.index:
        data = []
        for c in df.columns:
            item = df.ix[i][c]
            if c != 'Principle link':
                data.append(item)
            else:
                data.append('')
        principles.append(data)
    data = {}
    data['principles'] = principles
    cdata = json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4)
    return Response(cdata,  mimetype='application/json')

def getbestpractice(thistabname):
    xl = pd.ExcelFile(MATRIX)
    df = ''
    for tabname in xl.sheet_names:
        #if tabname != 'CONTENTS':
        if tabname == thistabname:
            df = pd.read_excel(MATRIX, sheetname=tabname, header=1, skiprows=0)

    bestpr = []
    fields = ['BEST PRACTICE']
    for x in df[fields].index:
        thisvalue = str(df[fields].ix[x][0])
        if thisvalue != 'nan':
            bestpr.append(thisvalue)
    data = {}
    data['bestpractice'] = bestpr
    cdata = json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4)
    return Response(cdata,  mimetype='application/json')

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
            check = re.match('Unnamed', colname)
            if not check:
                columns.append(colname)
    alltopics['topics'] = columns
    cdata = json.dumps(alltopics, ensure_ascii=False, sort_keys=True, indent=4)
    return cdata

def subtopics(thistabname):
    alltopics = {}
    xl = pd.ExcelFile(MATRIX)
    df = ''
    for tabname in xl.sheet_names:
        #if tabname != 'CONTENTS':
        if tabname == thistabname:
            df = pd.read_excel(MATRIX, sheetname=tabname, header=1, skiprows=0)

    # Make order FAIR
    fields = ['Findable', 'Accessible', 'Interoperable', 'Reusable']
    phrase = "Guidelines to make your data"
    topics = {}
    for name in fields:
        x = df.ix[0] == name
        y = x[x == True]
        longname = "%s %s" % (phrase, name.lower())
        topics[longname] = y.index.tolist()
    alltopics['topics'] = topics
    fullfields = []
    for name in fields:
	fullfields.append("%s %s" % (phrase, name.lower()))
    alltopics['order'] = fullfields
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

@app.route("/bestpractice", methods=['GET', 'POST'])
def bestpractice():
    newfilterparams = []
    discipline = ''
    try:
         qinput = json.loads( request.data )
         for name in qinput.keys():
             newfilterparams.append(str(name))
    except:
	discipline = request.args.get('discipline')
	if not discipline:
            return 'no data'

    params = filtertodict(newfilterparams)
    for name in params:
        if params[name] == 'discipline':
            discipline = name
    return getbestpractice(discipline)

@app.route("/principles")
def principles():
    return getprinciples("HIGH-LEVEL PRINCIPLES")

@app.route("/xmlmatrix")
def export2xml():
    return Response(matrix2xml(), mimetype='text/xml')

@app.route("/verification")
def verify():
    c = read_contents("CONTENTS")
    topics = []
    columns = {}
    for name in c['name']:
        df = dataloader(name)
        for c in df.columns:
            try:
                columns[c] = columns[c] + 1
            except:
                columns[c] = 1

    ver = ''
    for c in sorted(columns):
        check = re.match('Unnamed', c)
        if not check:
            ver = ver + "%s| %s<br />\n" % (c, columns[c])
    return str(ver)

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

    # MOD
    try:
        outmatrix = mainfilter(df, filtertodict(newfilterparams))
        data = json.dumps(outmatrix, ensure_ascii=False, sort_keys=True, indent=4)
        return Response(data,  mimetype='application/json')
    except:
	c = read_contents("CONTENTS")
	disc = {}
	for name in c['name']:
	    if name != discipline:
		thiskey = "discipline:%s" % name
	        disc[thiskey] = 1
        return str(disc)

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
    return subtopics(maindiscipline)

if __name__ == '__main__':
    s = datacache(cachedir)
    app.run(host='0.0.0.0', port=8081)
