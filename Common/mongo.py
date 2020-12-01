# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : mongo
# @Date        : 2020/12/1 0001
# @Description : xjrw_chain_dashboard

import pymongo


class Mongo(object):
    def __init__(self, mg_addr):
        self.mg_addr = mg_addr
        self.mg_client = pymongo.MongoClient(self.mg_addr)
        self.dbs = self.get_db_list()
        self.cols = self.get_col_list()

    def get_db_list(self):
        return self.mg_client.list_database_names()

    def get_col_list(self):
        mg_cols = {}
        for mg_db in self.dbs:
            cols = mg_db.list_collection_names()
            mg_cols[mg_db] = cols
        return mg_cols

    def find_one(self, mg_col):
        return mg_col.find_one()

    def find(self, mg_col, limit=0):
        return mg_col.find()

