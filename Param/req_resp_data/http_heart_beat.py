# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : 01_heart_beat
# @Date        : 2020/12/5 0005
# @Description : xjrw_chain_dashboard

# HTTP_API_HEARTBEAT request data and response data
data = {
    "url": "/api/v1.0/headbeat",
    "header": {"Content-Type": "application/json",
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/85.0.4183.102 Safari/537.36'},

    # for case: heart_beat
    "heart_beat_shard_chain":
        {
            "request": {
                "type": "S",
                "chainKey": "0101",
                "nodeId": "12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBqs01",
                "time": "2020-01-01T00:00:00.927+08:00"
            },
            "response": {
                "code": 200,
                "message": "OK",
                "data": {},
            }
        },
    # for case: heart_beat_duplicated_data
    "heart_beat_duplicated_data":
        {
            "request": {
                "type": "S",
                "chainKey": "0101",
                "nodeId": "12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBqs01",
                "time": "2020-01-01T00:00:00.927+08:00"
            },
            "response": {
                "code": 200,
                "message": "OK",
                "data": {},
            }
        },
    # for case: heart_beat_update_data
    "heart_beat_update_data":
        {
            "request":
                [{
                    "type": "S",
                    "chainKey": "0101",
                    "nodeId": "12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBqs01",
                    "time": "2020-01-01T00:00:00.927+08:00"
                }, {
                    "type": "S",
                    "chainKey": "0101",
                    "nodeId": "12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBqs01",
                    "time": "2020-01-01T00:01:00.927+08:00"
                }, ],
            "response": {
                "code": 200,
                "message": "OK",
                "data": {},
            },
        },
    # for case: heart_beat_wrong_value_chain_type
    "heart_beat_wrong_value_chain_type":
        {
            "request": {
                "type": "A",
                "chainKey": "0101",
                "nodeId": "12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBqs01",
                "time": "2020-01-01T00:00:00.927+08:00"
            },
            "response": {
                "code": 400,
                "message": "error",
                "data": {},
            }
        },
    # for case: heart_beat_null_value_chain_type
    "heart_beat_null_value_chain_type":
        {
            "request": {
                "type": "",
                "chainKey": "0101",
                "nodeId": "12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBqs01",
                "time": "2020-01-01T00:00:00.927+08:00"
            },
            "response": {
                "code": 400,
                "message": "error",
                "data": {},
            }
        },
}
