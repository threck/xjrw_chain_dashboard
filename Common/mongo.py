# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : mongo
# @Date        : 2020/12/1 0001
# @Description : xjrw_chain_dashboard

import pymongo
from Common import log
from Common import common


class Mongo(object):

    def __init__(self, mg_addr, db, col):
        self.log = log.Log('mongo')
        self.mg_addr = mg_addr
        self.mg_client = pymongo.MongoClient(self.mg_addr)
        self.db = db
        self.col = col
        self.dbs = self.get_db_list()
        self.cols = self.get_col_list()
        if self._db_or_col_exist():
            self.print_mongo_info()
        else:
            raise Exception('creat Mongo object failed: db or cols not exist')
        self.mg_db = self.mg_client[db]
        self.mg_col = self.mg_db[col]

    def _db_or_col_exist(self):
        if self.db not in self.dbs:
            self.log.error(f'db name:[ {self.db} ] is wrong! please use these exist dbs: {self.dbs}!')
            return False
        elif self.col not in self.cols[self.db]:
            self.log.error(f'col name:[ {self.col} ] in [ {self.db} ] is wrong! please use these exist cols: {self.cols[self.db]}!')
            return False
        else:
            return True

    def print_mongo_info(self):
        self.log.info(f'MONGO ADDR: {self.mg_addr}')
        self.log.info(f'DBS: {self.dbs}')
        self.log.info(f'COLS: {self.cols}')

    def get_db_list(self):
        return self.mg_client.list_database_names()

    def get_col_list(self):
        mg_cols = {}
        for db in self.dbs:
            mg_db = self.mg_client[db]
            cols = mg_db.list_collection_names()
            mg_cols[db] = cols
        return mg_cols

    def find_one(self):
        data = self.mg_col.find_one()
        self.log.info(f'get data in mongo[{self.db}][{self.col}] only_one: {data}')
        return data

    def find(self, limit=0):
        if limit == 0:
            data = list(self.mg_col.find({}, {"_id": 0}))
        else:
            data = list(self.mg_col.find({}, {"_id": 0}).limit(limit))
        self.log.info(f'get data in mongo[{self.db}][{self.col}](limit={limit}): {data}')
        return data

    def clear_col_data(self):
        x = self.mg_col.delete_many({})
        del_count = x.deleted_count
        self.log.info(f'mongo db [{self.db}][{self.col}]: {del_count} docs deleted!!')
        return del_count

    def insert_col_data_one(self, data):
        if isinstance(data, dict):
            x = self.mg_col.insert_one(data)
            self.log.info(f'mongo db [{self.db}][{self.col}] inserted data:{data}')
            return x.inserted_id
        else:
            raise Exception(self.log.error('please insert a dict type data. e.g. {"a":1, "b":2}'))

    def insert_col_data(self, data):
        if isinstance(data, list) and isinstance(data[0], dict):
            x = self.mg_col.insert_one(data)
            self.log.info(f'mongo db [{self.db}][{self.col}] inserted data:{data}')
            return x.inserted_id
        else:
            raise Exception(self.log.error('please insert a list type data with elements of dict. e.g. [{"a":1, "b":2}]'))


if __name__ == '__main__':
    # mg_db = mg_client[db_list[0]]
    # mg_col = mg_db["test_fangchao"]
    addr = 'mongodb://poolwebtest:xjrw2020@118.24.168.230:27017/poolwebtest'
    addr2 = 'mongodb://pynxtest:xjrw2020@118.24.168.230:27017,118.24.168.230:27018,118.24.168.230:27019/pynxtest'
    mg = Mongo(addr2, 'pynxtest2', 'nodes')

    print(mg.dbs)
    print(mg.cols)
    print()
    print(mg.find(limit=0))
    data = {
        "keyId" : "a-2",
        "lastTime" : common.current_time_iso(),
        "number" : "2",
        "type" : "a",
    }
    mg.insert_col_data_one(data)

    # mg_db = mg.mg_client['pynxtest']
    # mg_col = mg_db['node']
    # print(list(mg_col.find()))

