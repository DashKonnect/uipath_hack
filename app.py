from jinja2 import Template
from flask import Flask, request, render_template, jsonify
import webbrowser
import json
import os

app = Flask(__name__)

one_col_width = 0

def argmin(values):
    return values.index(min(values))

def column(arr, i):
    return [row[i] for row in arr]

def group_by_y_axis(components):
    rows = []
    while len(components):
        row = []
        component = components[0]
        y = component['y']
        height = component['height']
        y_end = y + height
        for other_component in components[1:]:
            o_y = other_component['y']
            o_height = other_component['height']
            other_y_end = o_y + o_height
            if y_end-50 < other_y_end < y_end+50:
                row.append(other_component)
        
        row.append(component)
        [components.remove(element) for element in row]
        rows.append(row)
    
    rows.sort(key = lambda x: x[0]['y'] + x[0]['height'])
    return rows

# def spilt_main_rows(row):
#     sum = row.sum(key = lambda x: x['width'])
#     percent = sum / total_width
#     return True if percent >= 0.9 else False

def get_cols_nums(component):
    start_x = component['x']
    end_x = component['x'] + component['width']
    return ( start_x / one_col_width, end_x / one_col_width )

def create_column(start, end):
    return {
        "type": "column",
        "size": end - start + 1,
        "start": start,
        "offset": 0,
        "children": []
    }

def create_component(c_type, width, height):
    return {
                "type": c_type,
                "width" : width,
                "height": height
            }

def column_with_component(component):
    c_type, width, height = component['type'], component['width'], component['height']
    column_nums = get_cols_nums(component)
    dsl_column = create_column(*column_nums)
    dsl_component = create_component(c_type, width, height)
    dsl_column["children"].append(dsl_component)
    return dsl_column

def create_row():
    return {
        "type": "row",
        "children": []
    }

def one_column_width(width):
    return width / 12

""" {
    width: 500,
    height: 300,
    components: [
        {
            x: 200,
            y: 200,
            width: 100,
            height: 100,
            type: "image"
        }
    ]
} """
def get_response(data):
    global one_col_width
    full_width = data['width']
    one_col_width = one_column_width(full_width)
    components = data['components']
    rows = group_by_y_axis(components)
    # main_rows = filter(rows, spilt_main_rows)
        
    dsl = []
    for row in rows:
        new_row = create_row()
        column_list = list(range(1,13))
        children = new_row['children']
        for component in row:
            dsl_column = column_with_component(component)
            children.append(dsl_column)
            start_col = dsl_column['start']
            end_col = dsl_column['start'] + dsl_column['size']
            column_list = filter(lambda x: x not in list(range(start_col, end_col)), column_list)

        for col_number in column_list:
            dsl_column = create_column(col_number, col_number)
            children.insert(col_number-1, dsl_column)

        dsl.append(new_row)

    # return jsonify(dsl)
    return render_template('index.html', dsl=dsl)



@app.route('/', methods = ['POST'])
def hello_world():
    data = request.get_json()
    return get_response(data)

@app.route('/test', methods = ['GET'])
def test():
    with open("dsl.json") as file:
        dsl = json.loads(file.read())
    return render_template('index.html', dsl = dsl)