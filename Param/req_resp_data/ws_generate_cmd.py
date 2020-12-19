# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : ws_generate_cmd
# @Date        : 2020/12/5 0005
# @Description : xjrw_chain_dashboard

# WEBSOCKET_API_GENERATE_CMD request data and response data
data = {
    # for case: generate_cmd_single_request_shard_chain
    "generate_cmd_single_request_shard_chain":
        {
            "post_request": [{
                "type": "S",
                "chainKey": "0101",
                "nodeId": "12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBqs01",
                "time": "2020-01-01T00:00:00.927+08:00"
            }, {
                "type": "S",
                "chainKey": "0102",
                "nodeId": "12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBqs02",
                "time": "2020-01-01T00:00:03.927+08:00"
            }],
            "post_response": {
                "code": 200,
                "message": "OK",
                "data": {},
                # "data": {"key": "", "params": {}},
            },
            "ws_request": {
                "uri": "cmd",
                "body":
                    {
                        "type": "S",
                        "cmd": {"key": "transfer", "params": {"amount": 10}}
                    },
                "msgId": "11234567890123456789012345678901"
            },
            "ws_response": {
                "uri": "cmd",
                "body": {},
                "msgId": "11234567890123456789012345678901"
            },
        },

    "generate_cmd_with_no_nodes":
        {
            "ws_request": {
                "uri": "cmd",
                "body":
                    {
                        "type": "S",
                        "cmd": {"key": "transfer", "params": {"amount": 10}}
                    },
                "msgId": "11234567890123456789012345678901"
            },
            "ws_response": {
                "uri": "cmd",
                "body": {},
                "error": {"code": 400, "message": "操作失败"},
                "msgId": "11234567890123456789012345678901"
            },
        },

    # for case: generate_cmd_multi_request_in_15s_shard_chain
    "generate_cmd_multi_request_in_15s_shard_chain":
        {
            "interval": 15,
            "post_request": [{
                "type": "S",
                "chainKey": "0101",
                "nodeId": "22D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBab01",
                "time": "2020-01-01T00:00:00.927+08:00"
            }, {
                "type": "S",
                "chainKey": "0102",
                "nodeId": "22D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBab02",
                "time": "2020-01-01T00:00:03.927+08:00"
            }],
            "post_response": {
                "code": 200,
                "message": "OK",
                "data": {},
                # "data": {"key": "", "params": {}},
            },
            "ws_request": [{
                "uri": "cmd",
                "body":
                    {
                        "type": "S",
                        "cmd": {"key": "transfer", "params": {"amount": 10}}
                    },
                "msgId": "11234567890123456789012345678901"
            }, {
                "uri": "cmd",
                "body":
                    {
                        "type": "S",
                        "cmd": {"key": "transfer", "params": {"amount": 10}}
                    },
                "msgId": "11234567890123456789012345678902"
            }],
            "ws_response": [{
                "uri": "cmd",
                "body": {},
                "msgId": "11234567890123456789012345678901"
            }, {
                "uri": "cmd",
                "body": {},
                "error": {"code": 400, "message": "操作失败"},
                "msgId": "11234567890123456789012345678902"
            }]

        },

    # for case: generate_cmd_multi_request_after_15s_shard_chain
    "generate_cmd_multi_request_after_15s_shard_chain":
        {
            "interval": 15,
            "post_request": [{
                "type": "S",
                "chainKey": "0101",
                "nodeId": "22D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBab01",
                "time": "2020-01-01T00:00:00.927+08:00"
            }, {
                "type": "S",
                "chainKey": "0102",
                "nodeId": "22D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBab02",
                "time": "2020-01-01T00:00:03.927+08:00"
            }],
            "post_response": {
                "code": 200,
                "message": "OK",
                "data": {},
            },
            "ws_request": [{
                "uri": "cmd",
                "body":
                    {
                        "type": "S",
                        "cmd": {"key": "transfer", "params": {"amount": 10}}
                    },
                "msgId": "11234567890123456789012345678901"
            }, {
                "uri": "cmd",
                "body":
                    {
                        "type": "S",
                        "cmd": {"key": "transfer", "params": {"amount": 10}}
                    },
                "msgId": "11234567890123456789012345678902"
            }],
            "ws_response": [{
                "uri": "cmd",
                "body": {},
                "msgId": "11234567890123456789012345678901"
            }, {
                "uri": "cmd",
                "body": {},
                "msgId": "11234567890123456789012345678902"
            }]
        },
}
