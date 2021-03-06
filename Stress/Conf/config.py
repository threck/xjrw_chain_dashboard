# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : config.py
# @Date        : 2020/12/14 0014
# @Description : xjrw_chain_dashboard

#####################
# Server info
#####################
IP = "192.168.1.15"
# IP = "172.16.8.109"
PORT = 8678
# POST_URL = 'http://172.70.16.105:8899/api/v1.0/block'
POST_URL = 'http://127.0.0.1:8888/api/v1.0/block'
# POST_URL = 'http://172.16.8.105:8888/api/v1.0/block'
# POST_URL = 'http://172.16.7.182:8899/api/v1.0/block'
# CPU_NUMBER = 3
CPU_NUMBER = 32


#####################
# Chain info
#####################
CHAIN_NU_TOTAL = {"R": 4, "S": 16}
CHAIN_NU_LOCAL = {"R": 4, "S": 16}
SS_TRADE_NU = 5

#####################
# Chain post request status mark
#####################
B_OVER_MARK = 'b_over'
R_OVER_MARK = 'r_over'
S_OVER_MARK = 's_over'
B_START_MARK = 'b_start'
R_START_MARK = 'r_start'
S_START_MARK = 's_start'

#####################
# Send times control
#####################
# if you want loop [n] time, you should set the value to [n+1]
# if you want to run forever, you should set the value to 0
STRESS_LOOP_TIME = 0
# set the loop interval time between every B->R->S post send cycle.
STRESS_LOOP_INTERVAL = 2
