from collections import defaultdict
from datetime import datetime

import pandas
import requests
from flask import json


def url():
    return 'http://123.139.89.242:60000/api/rxframes'



def params_generate(_page, _perPage, _sortDir, _sortField):
    params = []
    params.append(['_page', _page])
    params.append(['_perPage', _perPage])
    params.append(['_sortDir', _sortDir])
    params.append(['_sortField', _sortField])
    print(params)
    return params

def generate_table():
    headers = {
        'Authorization': 'Digest username="admin", realm="lorawan-server", nonce="1926482c41e2ef6920550754dd337b9d", uri="/api/rxframes?_page=1&_perPage=30&_sortDir=DESC&_sortField=datetime", response="49f64634dce3c378e78113455f32ecb4"'
    }
    response = requests.get(url(), headers=headers, params=params_generate(1, 30, 'DESC', 'datetime'))
    data=json.loads(response.content)

    # 创建一个字典对象，以devaddr作为key，默认值为一个空列表
    grouped_data = {}

    # 遍历原始列表中的元素，将每个元素添加到它对应的devaddr的列表中
    for item in data:
        item['datetime'] = datetime.strptime(item['datetime'], "%Y-%m-%dT%H:%M:%S.%fZ")
        if item['devaddr'] not in grouped_data:
            grouped_data[item['devaddr']]=[]
        grouped_data[item['devaddr']].append(item)

    # 对每个devaddr的列表按照datetime从新到旧排序
    for devaddr in grouped_data:
        grouped_data[devaddr].sort(key=lambda x: x['datetime'], reverse=True)

    result=[]
    for key in grouped_data:
        item=grouped_data.get(key)[0]
        result.append([item['devaddr'],item['datetime']])

    return pandas.DataFrame(result, columns=['devaddr','datetime']).to_html()
