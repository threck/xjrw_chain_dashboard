# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : config.py
# @Date        : 2020/12/14 0014
# @Description : xjrw_chain_dashboard

#####################
# Server info
#####################
IP = "192.168.0.30"
PORT = 5678
POST_URL = 'http://192.168.0.164:8888/api/v1.0/block'

#####################
# Chain info
#####################
CHAIN_NU_TOTAL = {"R": 2, "S": 4}
CHAIN_NU_LOCAL = {"R": 2, "S": 4}
SS_TRADE_NU = 3

#####################
# Chain post request status mark
#####################
R_READY_MARK = 'r_ready'
S_READY_MARK = 's_ready'

#####################
# Send times control
#####################
# if you want loop [n] time, you should set the value to [n+1]
# if you want to run forever, you should set the value to 0
STRESS_LOOP_TIME = 0
# set the loop interval time between every B->R->S post send cycle.
STRESS_LOOP_INTERVAL = 2
