#!/usr/bin/python

import re
import sys
import json
from flask import Flask, redirect, make_response, Response, render_template, request, send_from_directory
import requests
import logging
app = Flask(__name__)

root = "http://localhost:5000"
@app.route('/test', methods=['GET', 'POST'])
def test():
    params = request.args 
    url = root
    url+= "/mainfilter"
    if request.data:
	qinput = json.loads( request.data )
        resp = requests.post(url=url, data=request.data)
	return resp.text
        data = json.loads(resp.text)
	return 'test'
        return Response(resp.text,  mimetype='application/json')
	#cdata = json.dumps(qinput, ensure_ascii=False, sort_keys=True, indent=4)
	#logging.info( "test");
        #return Response(cdata,  mimetype='application/json')
    return 'test1'

@app.route('/filter', methods=['GET', 'POST'])
def customfilter():
    params = request.args
    url = root
    url+= "/mainfilter"
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    return Response(resp.text,  mimetype='application/json')

@app.route('/list', methods=['GET', 'POST'])
def list():
    params = request.args
    url = root
    url+= "/list"
    if request.data:
        qinput = json.loads( request.data )
        resp = requests.post(url=url, data=request.data)
	data = json.loads(resp.text)
    else:
        resp = requests.get(url=url, params=params)
        data = json.loads(resp.text)
    return Response(resp.text,  mimetype='application/json')

@app.route('/topics', methods=['GET', 'POST'])
def apitopics():
    params = request.args
    url = root
    url+= "/topics"
    if request.data:
        qinput = json.loads( request.data )
        resp = requests.post(url=url, data=request.data)
	return str(resp.text)
        data = json.loads(resp.text)
	return Response(data,  mimetype='application/json')
    else:
        resp = requests.get(url=url, params=params)
        data = json.loads(resp.text)
        return Response(resp.text,  mimetype='application/json')

@app.route('/contents', methods=['GET', 'POST'])
def content():
    params = request.args
    url = root
    url+= "/contents"
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    return Response(resp.text,  mimetype='application/json')

@app.route('/policies', methods=['GET', 'POST'])
def policies():
    params = request.args
    url = root
    url+= "/policies"
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    return Response(resp.text,  mimetype='application/json')

@app.route('/', methods=['GET', 'POST'])
def main():
    params = request.args
    url = root
    resp = requests.get(url=url, params=params)
#    return resp.text
    data = json.loads(resp.text)
    return Response(data,  mimetype='application/json')

if __name__ == '__main__':
    app.run()
