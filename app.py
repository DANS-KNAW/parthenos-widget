from __future__ import print_function, absolute_import

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import collections
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
        cellxml = ''
        for col in df.columns:
            #print "\t%s %s" % (col, str(thisindex))
            colname = col
            colname = colname.replace("\n", '_', 10)
            colname = colname.replace('&', '&amp;', 30)
	    colname = colname.replace(',', '', 30)
	    colname = colname.replace(' ', '_', 30)
            if re.search(r"^(\d)", colname):
                colname = "_" + colname

            value = str(df.ix[thisindex][col])
            value = value.replace('&','&amp;').decode('utf-8')
            if value == 'nan':
                value = ''
            else:
                #tmpxml = tmpxml + "\n\t\t<column name=\"%s\">%s</column>" % (colname, value)
                if not re.search('Unnamed', colname):
                    cellxml = cellxml + "\n\t\t<%s>%s</%s>" % (colname, value, colname)
            #print col
            try:
                allvalues[str(col)] = ''
            except:
                skip = 1

        if cellxml:
            tmpxml = tmpxml + "\t<item>%s\n\t</item>\n" % cellxml
                
        finalvalues = []
        for item in sorted(allvalues):
            finalvalues.append(item)
    return tmpxml

def matrix2xml():
    sheetid = 0
    xmlcontent = "<?xml version=\"1.0\"?>"
    xmlcontent = xmlcontent + "\n<Disciplines>"
    data = read_contents("CONTENTS")
    content = {}
    for index in data.index:
        row = data.ix[index]
        if str(row[1]) != 'nan':
            content[row[0]] = row[1]
        else:
            content[row[0]] = ''

    for dname in content:
	showname = dname
	showname = showname.replace(' ', '_', 30)

	df = dataloader(dname)
        if sheetid:
            xmlcontent = xmlcontent + "\n\t<%s>\n" % showname
            tmpxml = frametoxml(df)
            xmlcontent =  xmlcontent + tmpxml + "\t</%s>" % showname
        sheetid = sheetid + 1
    xmlcontent = xmlcontent + "\n</Disciplines>"
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
    return render_template('widget.html')

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
    return getprinciples("PARTHENOS guidelines")

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
    if not re.search('topic', str(newfilterparams)):
	return 'no topic'

    cache = {}
    #newfilterparams = ["community:RESEARCH COMMUNITY","discipline:SOCIAL SCIENCE","topic:CITATION GUIDELINES", "topic:PRIVACY AND SENSITIVE DATA"]
    params = filtertodict(newfilterparams)
    discipline = ''
    searchfilter = {}
    for name in params:
        if params[name] == 'discipline':
            discipline = name
	    df = dataloader(discipline)
	else:
	    if params[name] == 'topic':
	        searchfilter[name] = params[name]

    if discipline == '':
        for name in params: 
            if params[name] == 'community':
                discipline = name
		df = dataloader(discipline)
		cache[discipline] = df

    # MOD
    common = {}
    result = {}
    datatopics = {}
    noresult = "No results for this topic. Here you can find suggestions from other disciplines"
    for topic in searchfilter:
	thisfilter = {}
	found = {}
	thisfilter[topic] = searchfilter[topic]
	(outmatrix, fair) = mainfilter(df, thisfilter) #filtertodict(newfilterparams))

	# FAIR
	try:
            #(outmatrix, fair) = mainfilter(df, thisfilter) #filtertodict(newfilterparams))
	    if outmatrix[topic]:
		outmatrix['result'] = 'found'
		outmatrix['status'] = 'ok'
	 	topics = []
		for utopic in fair:
		    topics.append(utopic)
		outmatrix['topics'] = topics
		found[topic] = fair[topic]
		datatopics[topic] = fair[topic]
		#result[fair[topic]] = outmatrix #{ 'result': 'found', 'status': 'ok', 'data': outmatrix[topic] } ]
		result[topic] = outmatrix[topic]
	except:
	    skip = 1

	if not topic in found:
	    result[topic] = { 'result': noresult, 'status': 'not found', 'topic': fair[topic] } 
	    datatopics[topic] = fair[topic]
	    c = read_contents("CONTENTS")
	    disc = {}
	    common = collections.OrderedDict()
	    for name in c['name']:
	        if name != discipline:
		    if name not in cache:
		        cache[name] = dataloader(name)
		    try:
		        (outmatrix, fair) = mainfilter(cache[name], thisfilter)
			dmatrix = {}
			dmatrix[name] = outmatrix[topic]
		        common[topic] = dmatrix
		    except:
		        skip = 1
		
    other = {}
    if result:
        other['result'] = result
    if common:
        other['other'] = common

    grouptopics = {} 
    for topic in datatopics:
	if datatopics[topic] in grouptopics:
	    groupx = grouptopics[datatopics[topic]]
	    groupx.append(topic)
	    grouptopics[datatopics[topic]] = groupx
	else:
	    grouptopics[datatopics[topic]] = [ topic ]

    other['topics'] = grouptopics
    data = json.dumps(other, ensure_ascii=False, sort_keys=True, indent=4)
    return Response(data,  mimetype='application/json')

@app.route("/contents", methods=['GET', 'POST'])
def webcontents():
    return contents('CONTENTS')
    if request.data:
        qinput = json.loads( request.data )
        if 'selected' in qinput:
	    return 'All disciplines'
	return 'All disciplines selected'
    else:
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
