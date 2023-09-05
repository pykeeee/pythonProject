import os

import flask
import requests
from flask import Flask, json
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
    return flask.render_template('analyze_data.html',
                                 )

@app.route('/do_analyze_data', methods=["GET"])
def do_analyze_data():
    params = request.args
    print(params)
    return generate_table(params.get('only_warn','否'))

@app.route('/champion_pool_analyze', methods=["POST"])
def champion_pool_analyze():
    print(request.data)
    params = json.loads(request.data)
    print(request)
    print(params)
    enemy_top = params.get('enemy_top', None)
    enemy_jungle = params.get('enemy_jungle', None)
    enemy_middle = params.get('enemy_middle', None)
    enemy_bottom = params.get('enemy_bottom', None)
    enemy_support = params.get('enemy_support', None)
    team_top = params.get('team_top', None)
    team_jungle = params.get('team_jungle', None)
    team_middle = params.get('team_middle', None)
    team_bottom = params.get('team_bottom', None)
    team_support = params.get('team_support', None)
    enemy_chosen_dic = {'top': enemy_top, 'jungle': enemy_jungle, 'middle': enemy_middle, 'bottom': enemy_bottom,
                        'support': enemy_support}
    team_chosen_dic = {'top': team_top, 'jungle': team_jungle, 'middle': team_middle, 'bottom': team_bottom,
                       'support': team_support}
    patch=params.get('patch', None)
    champion_pool = []
    try:
        champion_pool=params.get('champion_pool')
        for item in champion_pool:
            item['champion']=constant.champions_cid_dic[item.get('champion')]
    except BaseException as e:
        rt = {'html': '所选英雄错误，请正确输入您想选的英雄（从下拉框选择） \n '+str(e)}
        print(rt)
        return rt
    tier = params['tier']
    region = params['region']
    return champion_pool_analyze_html(patch, champion_pool, tier, region, enemy_chosen_dic, team_chosen_dic)
def read(path):
    with open(path, "r", encoding='utf-8') as path_open:
        return path_open.read()
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=port,debug=True)