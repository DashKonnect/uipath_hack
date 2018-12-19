from jinja2 import Template
from flask import Flask, request, render_template
import webbrowser
import os

app = Flask(__name__)

def argmin(values):
    return values.index(min(values))

def column(arr, i):
    return [row[i] for row in arr]


def get_response(data):

    # TODO: get area of each
    # sort by area
    # start rendering fomn top
    # see which are smallest
    # see how many columns they belong to
    # see how many companions it has and how many columns they require
    # check if its nested by checking for bigger siblings
    # check for siblings below or above
        

    return render_template('index.html', print_rows=print_rows)



@app.route('/', methods = ['GET'])
def hello_world():
    data = request.args['data'][:-1]
    return get_response(data)