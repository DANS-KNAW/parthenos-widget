#!/usr/bin/python

import re
import sys
import pandas as pd
import numpy as np
import json
from flask import Flask, redirect, make_response, Response, render_template, request, send_from_directory
from parthenos.settings import MATRIX
from parthenos.core.datatojson import *
app = Flask(__name__)

path = "/var/www/parthenos/matrix.xlsx"
majorkey = "POLICY"
location = 'COUNTRY'

def contents(tabname):
    path = "/var/www/parthenos/matrixc.xlsx"
    df = pd.read_excel(path, sheetname=tabname, header=None, skiprows=0)
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
    return Response(cdata,  mimetype='application/json')

def processor():
    path = "/var/www/parthenos/matrix.xlsx"
    policy = "ADS - Archaeology Data Service"
    if request.args.get('policy'):
	policy = request.args.get('policy')
    df = pd.read_excel(path, header = 1)
    d = df[df['POLICY'] == policy]
    dataset = d.transpose()
    data = json.dumps(dataset.to_json(), ensure_ascii=False, sort_keys=True, indent=4)
    return Response(data,  mimetype='application/json')

def policies():
    df = pd.read_excel(path, header = 1)
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
    return Response(datajson,  mimetype='application/json')

def list():
    xl = pd.ExcelFile(path)
    tabs = xl.sheet_names
    tablist = {}
    tablist['data'] = tabs
    data = json.dumps(tablist, ensure_ascii=False, sort_keys=True, indent=4)
    return Response(data,  mimetype='application/json')

@app.route("/")
def main():
    return processor()

@app.route("/policies")
def webpolicies():
    return policies()

@app.route("/contents")
def webcontents():
    return contents('CONTENTS')

@app.route("/topics")
def webtopics():
    return gettopics('ARCHAEOLOGY')

@app.route("/list")
def showlist():
    return list()

if __name__ == '__main__':
    app.run()
