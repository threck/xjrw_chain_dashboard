# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : ws_get_block_info_realtime
# @Date        : 2020/12/5 0005
# @Description : xjrw_chain_dashboard


# WEBSOCKET_API_GET_BLOCK_INFO_REALTIME request data and response data
data = {
    # for case: get_real_chain_block_info (with http_block_reported api)
    "get_real_chain_block_info":
        {
            "post_request": [{
                "type": "R",
                "chainKey": "01",
                "nodeId": "12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBar01",
                "height": 1,
                "father": "0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a12f4217b0000",
                "hash": "0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a12f4217b0100",
                "gas": "gas",
                "vrf": "vrf",
                "time": "2020-12-08T16:03:04.872160+08:00",
                "interval": 1,
                "trans": 9,
                "size": 1,
                "lockHash": [{"type": "S", "chainkey": "0101", "height": 1}],
                "upHash": "HRfromR01",
                "downHash": "HBtoR01",
                "detail": {
                    "upStream": [{"fromkey": "R01", "tokey": "S0201", "hash": "HR01toS0201"},
                                 {"fromkey": "R01", "tokey": "S0301", "hash": "HR01toS0301"}
                                 ],
                    "downStream": [
                        {"fromkey": "R02", "tokey": "S0103", "hash": "HR02toS0103"},
                        {"fromkey": "R03", "tokey": "S0102", "hash": "HR03toS0102"},
                        {"fromkey": "R01", "tokey": "S0101", "hash": "HR01toS0101"}
                    ]
                }
            }, {
                "type": "R",
                "chainKey": "02",
                "nodeId": "12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBar02",
                "height": 1,
                "father": "0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a12f4217b0000",
                "hash": "0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a12f4217b0200",
                "gas": "gas",
                "vrf": "vrf",
                "time": "2020-12-08T16:03:04.872160+08:00",
                "interval": 1,
                "trans": 9,
                "size": 1,
                "lockHash": [{"type": "S", "chainkey": "0201", "height": 1}],
                "upHash": "HRfromR02",
                "downHash": "HBtoR02",
                "detail": {
                    "upStream": [{"fromkey": "R02", "tokey": "S0201", "hash": "HR02toS0201"},
                                 {"fromkey": "R02", "tokey": "S0301", "hash": "HR02toS0301"}
                                 ],
                    "downStream": [
                        {"fromkey": "R02", "tokey": "S0203", "hash": "HR02toS0203"},
                        {"fromkey": "R03", "tokey": "S0202", "hash": "HR03toS0202"},
                        {"fromkey": "R01", "tokey": "S0201", "hash": "HR01toS0201"}
                    ]
                }
            }, {
                "type": "R",
                "chainKey": "03",
                "nodeId": "12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBar03",
                "height": 1,
                "father": "0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a12f4217b0000",
                "hash": "0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a12f4217b0300",
                "gas": "gas",
                "vrf": "vrf",
                "time": "2020-12-08T16:03:04.872160+08:00",
                "interval": 1,
                "trans": 9,
                "size": 1,
                "lockHash": [{"type": "S", "chainkey": "0301", "height": 1}],
                "upHash": "HRfromR03",
                "downHash": "HBtoR03",
                "detail": {
                    "upStream": [{"fromkey": "R03", "tokey": "S0201", "hash": "HR03toS0201"},
                                 {"fromkey": "R03", "tokey": "S0301", "hash": "HR03toS0301"}
                                 ],
                    "downStream": [
                        {"fromkey": "R02", "tokey": "S0303", "hash": "HR02toS0303"},
                        {"fromkey": "R03", "tokey": "S0302", "hash": "HR03toS0302"},
                        {"fromkey": "R01", "tokey": "S0301", "hash": "HR01toS0301"}
                    ]
                }
            }],
            "post_response": [{
                "code": 200,
                "message": "OK",
                "data": {},
            }],
            "ws_request": [{
                "event": "block",
                "body": {},
                "msgId": "11234567890123456789012345678901"
            }],
            "ws_response": [{
                "event": "block",
                "body":
                    [{
                        "type": "R",  # [b|r|s], 链类型
                        "chainKey": "01",  # 链编号
                        "nodeId": "12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBar01",  # 节点id
                        "height": 1,  # 当前区块高度
                        "father": "0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a12f4217b0000",  # 父区块hash
                        "hash": "0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a12f4217b0100",  # 区块hash
                        "vrf": "vrf",  # VRF
                        "time": "2020-12-08T16:03:04.872160+08:00",  # 当前产生时间
                        "interval": 1,  # 出块间隔
                        "trans": 9,  # 交易数量
                        "size": 1,  # 区块大小
                    }],
                "msgId": "11234567890123456789012345678901"
            },
                {
                    "event": "block",
                    "body":
                        [{
                            "type": "R",  # [b|r|s], 链类型
                            "chainKey": "02",  # 链编号
                            "nodeId": "12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBar02",  # 节点id
                            "height": 1,  # 当前区块高度
                            "father": "0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a12f4217b0000",  # 父区块hash
                            "hash": "0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a12f4217b0200",  # 区块hash
                            "vrf": "vrf",  # VRF
                            "time": "2020-12-08T16:03:04.872160+08:00",  # 当前产生时间
                            "interval": 1,  # 出块间隔
                            "trans": 9,  # 交易数量
                            "size": 1,  # 区块大小
                        }],
                    "msgId": "11234567890123456789012345678901"
                },
                {
                    "event": "block",
                    "body":
                        [{
                            "type": "R",  # [b|r|s], 链类型
                            "chainKey": "03",  # 链编号
                            "nodeId": "12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBar03",  # 节点id
                            "height": 1,  # 当前区块高度
                            "father": "0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a12f4217b0000",  # 父区块hash
                            "hash": "0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a12f4217b0300",  # 区块hash
                            "vrf": "vrf",  # VRF
                            "time": "2020-12-08T16:03:04.872160+08:00",
                            "interval": 1,
                            "trans": 9,
                            "size": 1,
                        }],
                    "msgId": "11234567890123456789012345678901"
                },
                {
                    "event": "block",
                    "body": {},
                    "msgId": "11234567890123456789012345678901"
                }],
        },

    # for case: get_real_chain_block_info_with_wrong_post_request (with http_block_reported api)
    "get_real_chain_block_info_with_wrong_post_request":
        {
            "post_request": [{
                "type": "A",
                "chainKey": "01",
                "nodeId": "12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBar01",
                "height": 1,
                "father": "0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a12f4217b0000",
                "hash": "0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a12f4217b0100",
                "gas": "gas",
                "vrf": "vrf",
                "time": "2020-12-08T16:03:04.872160+08:00",
                "interval": 1,
                "trans": 9,
                "size": 1,
                "lockHash": [{"type": "S", "chainkey": "0101", "height": 1}],
                "upHash": "HRfromR01",
                "downHash": "HBtoR01",
                "detail": {
                    "upStream": [{"fromkey": "R01", "tokey": "S0201", "hash": "HR01toS0201"},
                                 {"fromkey": "R01", "tokey": "S0301", "hash": "HR01toS0301"}
                                 ],
                    "downStream": [
                        {"fromkey": "R02", "tokey": "S0103", "hash": "HR02toS0103"},
                        {"fromkey": "R03", "tokey": "S0102", "hash": "HR03toS0102"},
                        {"fromkey": "R01", "tokey": "S0101", "hash": "HR01toS0101"}
                    ]
                }
            }],
            "post_response": [{
                "code": 400,
                "message": "error",
                "data": {},
            }],
            "ws_request": [{
                "event": "block",
                "body": {},
                "msgId": "11234567890123456789012345678901"
            }],
            "ws_response": [{
                "event": "block",
                "body": {},
                "msgId": "11234567890123456789012345678901"
            }]
        },

    "get_real_chain_block_info_with_wrong_ws_book_event":
        {
            "ws_request": [{
                "event": "block123",
                "body": {},
                "msgId": "11234567890123456789012345678901"
            }],
            "ws_response": [{
                "uri": "",
                "body": "",
                "msgId": "11234567890123456789012345678901",
                "error": {"code": 400, "message": "websocket router path is not exitsts \n"}
            }]
        },

}
