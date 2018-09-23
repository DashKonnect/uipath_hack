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
    rows = []
    sorted_rows = []

    for line in data.split(";"):
        columns = line.split(",")
        rows.append(columns)

    y_column = column(rows,1)
    y_column = map(int, y_column)
    while y_column:
        el_index = argmin(y_column)
        element = rows[el_index]
        sorted_rows.append(element)
        del y_column[el_index]
        del rows[el_index]

    print_rows = []
    for i in range(len(sorted_rows)):
        row = sorted_rows[i]

        if i == 0:
            print_rows.append([row])
            continue


        prev_row = sorted_rows[i-1]
        current_y = int(row[1])
        prev_y = int(prev_row[1])

        

        if prev_y <= current_y <= prev_y + 50:
            print_rows[-1].append(row)
        else:
            print_rows.append([row])

    print(sorted_rows)
    print(print_rows)

    return render_template('index.html', print_rows=print_rows)



@app.route('/', methods = ['GET'])
def hello_world():
    data = request.args['data'][:-1]
    return get_response(data)