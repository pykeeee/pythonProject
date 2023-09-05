import os

import flask
import requests
from flask import Flask, json, send_from_directory
from flask import render_template
from flask import request
from pandas.io import common

from service import generate_table

app = Flask("WiseChooser")
port=5050

@app.route('/')
def hello_world():
    return flask.render_template('test.html'
                                 )

@app.route('/analyze_data', methods=["GET"])
def analyze_data():
    return flask.render_template('analyze_data.html'
                                 )

@app.route('/do_analyze_data', methods=["GET"])
def do_analyze_data():
    params = request.args
    print(params)
    return generate_table(params.get('only_warn','否'))


# 显示图片
@app.route('/pic')
def index():
    # 获取static/images/gallery文件夹中的所有文件名或文件路径
    image_names = os.listdir('static/images')
    return render_template('pic.html', image_names=image_names)

# 显示图片
@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory("static/images", filename)
def read(path):
    with open(path, "r", encoding='utf-8') as path_open:
        return path_open.read()

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=port,debug=True)