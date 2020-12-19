# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : ws_get_trade_info
# @Date        : 2020/12/5 0005
# @Description : xjrw_chain_dashboard

# WEBSOCKET_API_GET_TRADE_INFO request data and response data
data = {
    "url": "ws://192.168.0.164:9999/v1.0/conn",
    # for case: get_trade_info
    "get_trade_info":
        {
            "request": {
                "uri": "tranInfo",  # 命令地址
                "body": {
                    "hash": "123",  # 分片内交易hash
                },
                "msgId": "11234567890123456789012345678901"  # 32位随机字符串
            },
            "response": {
                "uri": "cmd",
                "body": {},
                "msgId": "11234567890123456789012345678901"  # 32位随机字符串
            },
        },

    # for case: get_trade_info_with_wrong_hash
    "get_trade_info_with_wrong_hash":
        {
            "request": {
                "uri": "tranInfo",  # 命令地址
                "body": {
                    "hash": "123",  # 分片内交易hash
                },
                "msgId": "11234567890123456789012345678901"  # 32位随机字符串
            },
            "response": {
                "uri": "cmd",
                "body": {},
                "msgId": "11234567890123456789012345678901"  # 32位随机字符串
            },
        },

    # for case: get_trade_info_with_wrong_hash
    "get_trade_info_with_null_hash":
        {
            "request": {
                "uri": "tranInfo",  # 命令地址
                "body": {
                    "hash": "",  # 分片内交易hash
                },
                "msgId": "11234567890123456789012345678901"  # 32位随机字符串
            },
            "response": {
                "uri": "cmd",
                "body": {},
                "msgId": "11234567890123456789012345678901"  # 32位随机字符串
            },
        },
}
