# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : mongo_test.py
# @Date        : 2020/12/1 0001
# @Description : xjrw_chain_dashboard

import pymongo
from Common import consts
import pytz
from datetime import datetime
# mg = 'mongodb://poolwebtest:xjrw2020@118.24.168.230:27017,118.24.168.230:27018,118.24.168.230:27019/poolwebtest'
mg = 'mongodb://pynxtest:pynxtest@139.186.84.15:27987,139.186.84.15:27988,139.186.84.15:27989/pynxtest'
# mg = 'mongodb://poolwebtest:xjrw2020@118.24.168.230:27018/poolwebtest‘
# mg = 'mongodb://poolwebtest:xjrw2020@118.24.168.230:27019/poolwebtest’


mg_client = pymongo.MongoClient(mg)
# 读取所有数据库
db = mg_client['pynxtest']
db_col = db['nodes']
tz = pytz.timezone(consts.TIME_ZONE_CITY_CHONGQING)

mydict = {
    "type": "S",
    "chainKey": "0101",
    "nodeId": "12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBqs01",
    "time": datetime.now(tz=tz)
}

x = db_col.insert_one(mydict)

y = db_col.find({}, {"_id": 0})
for i in y:
    print(i)

# print(list(x))
