from jinja2 import Template
from flask import Flask, request
import webbrowser

app = Flask(__name__)

with open('index.html','r') as file_h:
    html_template = file_h.read()
    template = Template(html_template)

def argmin(values):
    return values.index(min(values))

def column(arr, i):
    return [row[i] for row in arr]


def get_response(data):
    rows = []
    sorted_rows = []
# read the file
    # with open("hello.txt","r") as file_h:
        # for data in file_h:
        #     data = data.strip()
        #     columns = data.split(",")
        #     rows.append(columns)

    for line in data.split("\n"):
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

    output =  template.render(sorted_rows = sorted_rows)
    with open('output.html','w') as file_h:
        file_h.write(output)
    webbrowser.open('output.html')
    return output


@app.route('/', methods = ['POST'])
def hello_world():
    data = request.form['data']
    return get_response(data)

