#!/usr/bin/python

import re
import sys
import json
from flask import Flask, redirect, make_response, Response, render_template, request, send_from_directory
import requests
app = Flask(__name__)

root = "http://localhost:5000"
@app.route('/test', methods=['GET', 'POST'])
def test():
    return 'test'

@app.route('/list', methods=['GET', 'POST'])
def list():
    params = request.args
    url = root
    url+= "/list"
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    return Response(resp.text,  mimetype='application/json')

@app.route('/topics', methods=['GET', 'POST'])
def apitopics():
    params = request.args
    url = root
    url+= "/topics"
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
