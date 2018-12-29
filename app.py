from jinja2 import Template
from flask import Flask, request, render_template
import webbrowser
import json
import os

app = Flask(__name__)

def argmin(values):
    return values.index(min(values))

def column(arr, i):
    return [row[i] for row in arr]

def group_by_y_axis(components):
    rows = []
    for component in components:
        row = []
        y = component['y']
        height = component['height']
        y_end = y + height
        row.append(component)
        components -= component
        for other_component in components:
            o_y = component['y']
            o_height = component['height']
            other_y_end = o_y + o_height
            if y_end-50 < other_y_end < y_end+50:
                row += other_component
                components.append(other_component)
        rows.append(row)
    
    return rows.sort(key = lambda x: x[0]['y'] + x[0]['height'])

# def spilt_main_rows(row):
#     sum = row.sum(key = lambda x: x['width'])
#     percent = sum / total_width
#     return True if percent >= 0.9 else False

def get_cols_nums(component):
    start_x = component['x']
    end_x = component['x'] + component['width']
    return ( start_x / 12, end_x / 12 )

def create_column(start, end):
    return {
        "type": "column",
        "size": start - end + 1,
        "start": start,
        "children": []
    }

def create_component(c_type, width, height):
    return {
                "type": c_type,
                "width" : width,
                "height": height
            }

def column_with_component(component):
    c_type, width, height = component, component, component
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

def get_response(data):
    full_width = data
    components = []
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
            column_list.remove(range(start_col, end_col))

        for col_number in column_list:
            dsl_column = create_column(col_number, col_number)
            children.insert(col_number-1, dsl_column)

        dsl.append(new_row)

    return render_template('index.html', dsl=dsl)



@app.route('/', methods = ['GET'])
def hello_world():
    data = request.args['data'][:-1]
    return get_response(data)

@app.route('/test', methods = ['GET'])
def test():
    with open("dsl.json") as file:
        dsl = json.loads(file.read())
    return render_template('index.html', dsl = dsl)