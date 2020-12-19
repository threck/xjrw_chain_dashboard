# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : mwebsocket_test
# @Date        : 2020/12/3 0003
# @Description : xjrw_chain_dashboard

import random
import time
import json
import requests
from Common import mrequest

data = {
    "type":     "b",
    "number":   "10000%d" % random.randrange(0, 5),
    "id":       "10000%d" % random.randrange(0, 5),
    "height":   10,
    "father":   "fatherHash",
    "hash":     "hash",
    "vrf":      "vrf",
    "time":     time.time() * 1000 * 1000,
    "interval": random.randrange(0, 100),
    "trans":    random.randrange(0, 10000),
    "size":     random.randrange(0, 10000),
    "detail":   None,
}

j = json.dumps(obj=data)
print(type(j))
print(j)
print()

api_url = "http://192.168.0.164:9999/v1.0/block"
data = {
    "type":     "b",
    "number":   "10000%d" % random.randrange(0, 5),
    "id":       "10000%d" % random.randrange(0, 5),
    "height":   10,
    "father":   "fatherHash",
    "hash":     "hash",
    "vrf":      "vrf",
    "time":     time.time() * 1000 * 1000,
    "interval": random.randrange(0, 100),
    "trans":    random.randrange(0, 10000),
    "size":     random.randrange(0, 10000),
    "detail":   None,
}
data = json.dumps(data)
header = {"Content-Type": "application/json; charset=utf-8",
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"}
req = requests.post(url=api_url, params=data, headers=header)
print(req.status_code)
print(req.json())
print(req.text)
print(req.headers)
print()

req = mrequest.Request()
req2 = req.post_request(api_url, data, header)
print(req2)
