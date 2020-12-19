# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : ws_get_trading_group_info
# @Date        : 2020/12/5 0005
# @Description : xjrw_chain_dashboard


# WEBSOCKET_API_GET_TRADING_GROUP_INFO request data and response data
data = {
    "url": "ws:#192.168.0.164:9999/v1.0/conn",
    # for case: get_trading_group_info
    "get_trading_group_info":
        {
            "request": {
                "uri": "ssInfo",  # 命令地址
                "body": {
                    "height": 123,  # 区块高度
                    "fromShard": "SA",  # 存在的数据
                    "toShard": "SB",  # 存在的数据
                },  # 内容
                "msgId": "11234567890123456789012345678901"  # 32位随机字符串
            },
            "response": {
                "uri": "ssInfo",
                "body":
                    [{
                        "hash": 123,
                        "from": "SA",  # 发送方
                        "to": "SB",  # 接收方
                        "amount": 1,  # 数量
                    }],
                "error": {"code": "", "message": ""},  # 错误
                "msgId": "11234567890123456789012345678901"  # 32位随机字符串
            },
        },

    # for case: get_trading_group_info_with_wrong_height
    "get_trading_group_info_with_wrong_height":
        {
            "request": {
                "uri": "ssInfo",  # 命令地址
                "body": {
                    "height": 123,  # 区块高度
                    "fromShard": "SA",  # 存在的数据
                    "toShard": "SB",  # 存在的数据
                },  # 内容
                "msgId": "11234567890123456789012345678901"  # 32位随机字符串
            },
            "response": {
                "uri": "ssInfo",
                "body":
                    [{
                        "hash": 123,
                        "from": "SA",  # 发送方
                        "to": "SB",  # 接收方
                        "amount": 1,  # 数量
                    }],
                "error": {"code": "", "message": ""},  # 错误
                "msgId": "11234567890123456789012345678901"  # 32位随机字符串
            },
        },

    # for case: get_trading_group_info_with_null_height
    "get_trading_group_info_with_null_height":
        {
            "request": {
                "uri": "ssInfo",  # 命令地址
                "body": {
                    "height": 123,  # 区块高度
                    "fromShard": "SA",  # 存在的数据
                    "toShard": "SB",  # 存在的数据
                },  # 内容
                "msgId": "11234567890123456789012345678901"  # 32位随机字符串
            },
            "response": {
                "uri": "ssInfo",
                "body":
                    [{
                        "hash": 123,
                        "from": "SA",  # 发送方
                        "to": "SB",  # 接收方
                        "amount": 1,  # 数量
                    }],
                "error": {"code": "", "message": ""},  # 错误
                "msgId": "11234567890123456789012345678901"  # 32位随机字符串
            },
        },

    # for case: get_trading_group_info_with_wrong_fromShard
    "get_trading_group_info_with_wrong_fromShard":
        {
            "request": {
                "uri": "ssInfo",  # 命令地址
                "body": {
                    "height": 123,  # 区块高度
                    "fromShard": "SA",  # 存在的数据
                    "toShard": "SB",  # 存在的数据
                },  # 内容
                "msgId": "11234567890123456789012345678901"  # 32位随机字符串
            },
            "response": {
                "uri": "ssInfo",
                "body":
                    [{
                        "hash": 123,
                        "from": "SA",  # 发送方
                        "to": "SB",  # 接收方
                        "amount": 1,  # 数量
                    }],
                "error": {"code": "", "message": ""},  # 错误
                "msgId": "11234567890123456789012345678901"  # 32位随机字符串
            },
        },

    # for case: get_trading_group_info_with_null_fromShard
    "get_trading_group_info_with_null_fromShard":
        {
            "request": {
                "uri": "ssInfo",  # 命令地址
                "body": {
                    "height": 123,  # 区块高度
                    "fromShard": "SA",  # 存在的数据
                    "toShard": "SB",  # 存在的数据
                },  # 内容
                "msgId": "11234567890123456789012345678901"  # 32位随机字符串
            },
            "response": {
                "uri": "ssInfo",
                "body":
                    [{
                        "hash": 123,
                        "from": "SA",  # 发送方
                        "to": "SB",  # 接收方
                        "amount": 1,  # 数量
                    }],
                "error": {"code": "", "message": ""},  # 错误
                "msgId": "11234567890123456789012345678901"  # 32位随机字符串
            },
        },

    # for case: get_trading_group_info_with_wrong_toShard
    "get_trading_group_info_with_wrong_toShard":
        {
            "request": {
                "uri": "ssInfo",  # 命令地址
                "body": {
                    "height": 123,  # 区块高度
                    "fromShard": "SA",  # 存在的数据
                    "toShard": "SB",  # 存在的数据
                },  # 内容
                "msgId": "11234567890123456789012345678901"  # 32位随机字符串
            },
            "response": {
                "uri": "ssInfo",
                "body":
                    [{
                        "hash": 123,
                        "from": "SA",  # 发送方
                        "to": "SB",  # 接收方
                        "amount": 1,  # 数量
                    }],
                "error": {"code": "", "message": ""},  # 错误
                "msgId": "11234567890123456789012345678901"  # 32位随机字符串
            },
        },

    # for case: get_trading_group_info_with_null_toShard
    "get_trading_group_info_with_null_toShard":
        {
            "request": {
                "uri": "ssInfo",  # 命令地址
                "body": {
                    "height": 123,  # 区块高度
                    "fromShard": "SA",  # 存在的数据
                    "toShard": "SB",  # 存在的数据
                },  # 内容
                "msgId": "11234567890123456789012345678901"  # 32位随机字符串
            },
            "response": {
                "uri": "ssInfo",
                "body":
                    [{
                        "hash": 123,
                        "from": "SA",  # 发送方
                        "to": "SB",  # 接收方
                        "amount": 1,  # 数量
                    }],
                "error": {"code": "", "message": ""},  # 错误
                "msgId": "11234567890123456789012345678901"  # 32位随机字符串
            },
        },
}



