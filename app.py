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

    full_width = data
    components = []
    sorted_components_y = sorted_components_by_y_axis(sorted_components)
    #loop through components of first row
    

    # find number of columns



    return render_template('index.html', print_rows=print_rows)



@app.route('/', methods = ['GET'])
def hello_world():
    data = request.args['data'][:-1]
    return get_response(data)