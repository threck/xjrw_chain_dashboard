# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : mongo_test.py
# @Date        : 2020/12/1 0001
# @Description : xjrw_chain_dashboard

import pymongo

# mg = 'mongodb://poolwebtest:xjrw2020@118.24.168.230:27017,118.24.168.230:27018,118.24.168.230:27019/poolwebtest'
mg = 'mongodb://pynxtest:pynxtest@139.186.84.15:27987,139.186.84.15:27988,139.186.84.15:27989/pynxtest'
# mg = 'mongodb://poolwebtest:xjrw2020@118.24.168.230:27018/poolwebtest‘
# mg = 'mongodb://poolwebtest:xjrw2020@118.24.168.230:27019/poolwebtest’

mg_client = pymongo.MongoClient(mg)
# 读取所有数据库
db_list = mg_client.list_database_names()

# 使用数据库对象创建集合
mg_db = mg_client[db_list[0]]
mg_col = mg_db["test_fangchao"]
# 读取某数据库中所有集合
col_list = mg_db.list_collection_names()

# *查询某集合的数据
mg_col = mg_db['wallet_address']
x = mg_col.find_one()
for x in mg_col.find():
    print('wallet_address', x)
print()

# **高级查询
# 读取name字段 中第一个字母 ASCII值大于H的数据， 大于的修饰符条件: {"$gt": "H"}
my_query = {"name": {"$gt": "H"}}
my_query = {"address": {"$eq": '1576797979'}}
my_result = mg_col.find(my_query)
for x in my_result:
    print(x)
print()

# 读取 name 字段中第一个字母为 "R" 的数据，正则表达式修饰符条件为 {"$regex": "^R"}
my_query = {"name": {"$regex": "^R"}}
my_query = {"name": {"$regex": "^3"}}
my_result = mg_col.find(my_query)
for x in my_result:
    print(x)
print()

# 返回指定条数记录
my_query = {"status": {"$eq": 1}}
my_result = mg_col.find(my_query).limit(3)
for x in my_result:
    print('===', x)
    print('-->', x["_id"])
print()

# 不返回指定字段的记录
my_query = {"_id": 0}
my_result = mg_col.find({}, {"_id": 0}).limit(3)
for x in my_result:
    print('===', x)
print()

print(db_list)
print(col_list)
# print(list(x))
