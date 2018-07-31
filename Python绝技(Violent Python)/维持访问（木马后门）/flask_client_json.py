from http.client import HTTPConnection
import json

def http_post_json(ip,dict_data,port=5000):
    c = HTTPConnection(ip, port=port)

    #创建并写入HTTP头部数据
    headers = {}
    headers['Content-Type'] = 'application/json'

    #写入HTTP Body部分的JSON数据
    post_json_data = json.dumps(dict_data).encode('utf-8')

    #发起HTTP连接
    c.request('POST', '/server_json', body=post_json_data, headers=headers)

if __name__ == "__main__":
    json_data = {"from": "akjflw", "to":"fjlakdj", "amount": 3}
    http_post_json('202.100.1.224',json_data)