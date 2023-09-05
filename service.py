from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
import pandas
import requests
from flask import json
from matplotlib.font_manager import FontProperties


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


def parse_time(time_str):
    try:
        return datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
        return datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ')


def generate_table(only_warn='否'):
    print(only_warn)
    headers = {
        'Authorization': 'Digest username="admin", realm="lorawan-server", nonce="1926482c41e2ef6920550754dd337b9d", uri="/api/rxframes?_page=1&_perPage=30&_sortDir=DESC&_sortField=datetime", response="49f64634dce3c378e78113455f32ecb4"'
    }
    response = requests.get(url(), headers=headers, params=params_generate(1, 1000, 'DESC', 'datetime'))
    response_data = json.loads(response.content)

    # 创建一个字典对象，以devaddr作为key，默认值为一个空列表
    grouped_data = {}

    # 遍历原始列表中的元素，将每个元素添加到它对应的devaddr的列表中
    for item in response_data:
        item['datetime'] = parse_time(item['datetime'])
        if item['devaddr'] not in grouped_data:
            grouped_data[item['devaddr']] = []
        grouped_data[item['devaddr']].append(item)

    # 对每个devaddr的列表按照datetime从新到旧排序
    for devaddr in grouped_data:
        grouped_data[devaddr].sort(key=lambda x: x['datetime'], reverse=True)

    result = []
    for key in grouped_data:
        try:
            item = grouped_data.get(key)[0]
            data = item['data']
            last_eight = data[-8:]
            TH = int(str(last_eight[0:2]), 16)
            TL = int(str(last_eight[2:4]), 16)
            HH = int(str(last_eight[4:6]), 16)
            HL = int(str(last_eight[6:8]), 16)

            tem = ((TH & 7) * 256 + TL) * 0.0625
            hum = ((HH & 3) * 256 + HL) / 10
            warn = False
            if tem > 35:
                warn = True
            if only_warn=='否' or warn==True:
                result.append([item['devaddr'], item['datetime'], tem, hum, warn])

        except:
            pass

    return pandas.DataFrame(result, columns=['devaddr', '时间', '温度', '湿度', '是否报警']).to_html()

def draw():
    # 假设数据在这个列表中
    data = [
        {'时间': '2021-01-01', '温度': 10},
        {'时间': '2021-01-02', '温度': 11},
        {'时间': '2021-01-03', '温度': 12},
        {'时间': '2021-01-04', '温度': 13},
        {'时间': '2021-01-05', '温度': 12},
    ]

    # 将时间和温度分别保存到两个列表中
    time_list = [d['时间'] for d in data]
    temperature_list = [d['温度'] for d in data]

    # 画图
    fig, ax = plt.subplots()
    ax.plot(time_list, temperature_list)
    ax.set(xlabel='datetime', ylabel='温度', title='温度变化折线图')
    ax.grid()

    # 将绘制的图形保存到文件中
    fig.savefig("temperature.png")

if __name__ == "__main__":
    draw()
