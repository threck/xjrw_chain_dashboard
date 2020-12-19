# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : __init__
# @Date        : 2020/12/1 0001
# @Description : xjrw_chain_dashboard

import pytest
from Config import config
from Common import mongo
from Common import consts

@pytest.fixture()
def prepare_mongo_heart_report():
    conf = config.Config()
    mg_url = conf.mongodb_test
    mg = mongo.Mongo(mg_url, consts.MGDB, consts.MGDB_JDXX)
    mg.clear_col_data()
    return mg


@pytest.fixture()
def prepare_mongo_block_report():
    conf = config.Config()
    mg_url = conf.mongodb_test
    mg_sslsj = mongo.Mongo(mg_url, consts.MGDB, consts.MGDB_SSLSJ)
    mg_lslqksj = mongo.Mongo(mg_url, consts.MGDB, consts.MGDB_LSLQKSJ)
    mg_kfpjyzsj = mongo.Mongo(mg_url, consts.MGDB, consts.MGDB_KFPJYZSJ)
    mg_jysj = mongo.Mongo(mg_url, consts.MGDB, consts.MGDB_JYSJ)
    mg_sslsj.clear_col_data()
    mg_lslqksj.clear_col_data()
    mg_kfpjyzsj.clear_col_data()
    mg_jysj.clear_col_data()
    return dict(sslsj=mg_sslsj, lslqksj=mg_lslqksj, kfpjyzsj=mg_kfpjyzsj, jysj=mg_jysj)