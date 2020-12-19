# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : ws_get_block_info
# @Date        : 2020/12/5 0005
# @Description : xjrw_chain_dashboard

# WEBSOCKET_API_GET_BLOCK_INFO request data and response data
data = {
    "url": "ws://192.168.0.164:9999/v1.0/conn",
    # for case: get_block_info
    "get_block_info_of_shard_chain":
        {
            "request":
                {
                    "uri": "blockInfo",  # 命令地址
                    "body":
                        {
                            "type": "S",  # 链类型
                            "chainKey": "S0101",  # 链编号
                            "height": "1",  # 区块高度
                            "hash": "0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a12f4217b0100",  # 区块hash
                        },  # 内容
                    "msgId": "11234567890123456789012345678901"  # 32位随机字符串
                },
            "response": {
                "uri": "blockInfo",
                "body":
                    {
                        "type": "S",  # [b|r|s], 链类型
                        "chainKey": "S0101",  # 链编号
                        "nodeId": "String",  # 节点id
                        "height": "1",  # 当前区块高度
                        "father": "0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a12f4217b0000",  # 父区块hash
                        "hash": "0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a12f4217b0100",  # 区块hash
                        "vrf": "vrf",  # VRF
                        "time": "2020-12-08T16:03:04.872160+08:00",  # 当前产生时间
                        "interval": 1,  # 出块间隔
                        "trans": 9,  # 交易数量
                        "size": 1,  # 区块大小
                        "detail":
                            {
                                "upStream": [{"fromkey": "S0101", "tokey": "R01", "hash": "HS0101_S0102"},
                                             {"fromkey": "S0101", "tokey": "R01", "hash": "HS0101_S0103"},
                                             {"fromkey": "S0101", "tokey": "R02", "hash": "HS0101_S0201"},
                                             {"fromkey": "S0101", "tokey": "R02", "hash": "HS0101_S0203"},
                                             {"fromkey": "S0101", "tokey": "R03", "hash": "HS0101_S0301"},
                                             {"fromkey": "S0101", "tokey": "R03", "hash": "HS0101_S0302"},
                                             {"fromkey": "S0101", "tokey": "R03", "hash": "HS0101_S0303"}
                                             ],
                                "downStream": [],
                            }
                    },  # 单条数据
                "error": {"code": "", "message": ""},  # 错误
                "msgId": "11234567890123456789012345678901"  # 32位随机字符串
            },
        },

    # for case: get_block_info_of_shard_chain_only_post_type_chainkey_number
    "get_block_info_of_shard_chain_only_post_type_chainkey_number":
        {
            "request":
                {
                    "uri": "blockInfo",  # 命令地址
                    "body":
                        {
                            "type": "s",  # 链类型
                            "chainkey": "Sa1",  # 链编号
                            "number": "123",  # 区块高度
                            "hash": "hash",  # 区块hash
                        },  # 内容
                    "msgId": "11234567890123456789012345678901"  # 32位随机字符串
                },
            "response": {
                "uri": "blockInfo",
                "body":
                    {
                        "type": "String",  # [b|r|s], 链类型
                        "chainKey": "String",  # 链编号
                        "nodeId": "String",  # 节点id
                        "height": "Number",  # 当前区块高度
                        "father": "String",  # 父区块hash
                        "hash": "String",  # 区块hash
                        "vrf": "String",  # VRF
                        "time": "Date",  # 当前产生时间
                        "interval": "Number",  # 出块间隔
                        "trans": "Number",  # 交易数量
                        "size": "Number",  # 区块大小
                        "detail":
                            {
                                "upStream": [{"key": "String", "hash": "String"}],  # 上传hash组
                                "downStream": [{"key": "String", "hash": "String"}],  # 下传hash组
                            }
                    },  # 单条数据
                "error": {"code": "", "message": ""},  # 错误
                "msgId": "11234567890123456789012345678901"  # 32位随机字符串
            },
        },

    # for case: get_block_info_of_shard_chain_only_post_hash
    "get_block_info_of_shard_chain_only_post_hash":
        {
            "request":
                {
                    "uri": "blockInfo",  # 命令地址
                    "body":
                        {
                            "type": "s",  # 链类型
                            "chainkey": "Sa1",  # 链编号
                            "number": "123",  # 区块高度
                            "hash": "hash",  # 区块hash
                        },  # 内容
                    "msgId": "11234567890123456789012345678901"  # 32位随机字符串
                },
            "response": {
                "uri": "blockInfo",
                "body":
                    {
                        "type": "String",  # [b|r|s], 链类型
                        "chainKey": "String",  # 链编号
                        "nodeId": "String",  # 节点id
                        "height": "Number",  # 当前区块高度
                        "father": "String",  # 父区块hash
                        "hash": "String",  # 区块hash
                        "vrf": "String",  # VRF
                        "time": "Date",  # 当前产生时间
                        "interval": "Number",  # 出块间隔
                        "trans": "Number",  # 交易数量
                        "size": "Number",  # 区块大小
                        "detail":
                            {
                                "upStream": [{"key": "String", "hash": "String"}],  # 上传hash组
                                "downStream": [{"key": "String", "hash": "String"}],  # 下传hash组
                            }
                    },  # 单条数据
                "error": {"code": "", "message": ""},  # 错误
                "msgId": "11234567890123456789012345678901"  # 32位随机字符串
            },
        },

    # for case: get_block_info_of_relay_chain
    "get_block_info_of_relay_chain":
        {
            "request":
                {
                    "uri": "blockInfo",  # 命令地址
                    "body":
                        {
                            "type": "s",  # 链类型
                            "chainkey": "Sa1",  # 链编号
                            "number": "123",  # 区块高度
                            "hash": "hash",  # 区块hash
                        },  # 内容
                    "msgId": "11234567890123456789012345678901"  # 32位随机字符串
                },
            "response": {
                "uri": "blockInfo",
                "body":
                    {
                        "type": "String",  # [b|r|s], 链类型
                        "chainKey": "String",  # 链编号
                        "nodeId": "String",  # 节点id
                        "height": "Number",  # 当前区块高度
                        "father": "String",  # 父区块hash
                        "hash": "String",  # 区块hash
                        "vrf": "String",  # VRF
                        "time": "Date",  # 当前产生时间
                        "interval": "Number",  # 出块间隔
                        "trans": "Number",  # 交易数量
                        "size": "Number",  # 区块大小
                        "detail":
                            {
                                "upStream": [{"key": "String", "hash": "String"}],  # 上传hash组
                                "downStream": [{"key": "String", "hash": "String"}],  # 下传hash组
                            }
                    },  # 单条数据
                "error": {"code": "", "message": ""},  # 错误
                "msgId": "11234567890123456789012345678901"  # 32位随机字符串
            },
        },

    # for case: get_block_info_of_beacon_chain
    "get_block_info_of_beacon_chain":
        {
            "request":
                {
                    "uri": "blockInfo",  # 命令地址
                    "body":
                        {
                            "type": "s",  # 链类型
                            "chainkey": "Sa1",  # 链编号
                            "number": "123",  # 区块高度
                            "hash": "hash",  # 区块hash
                        },  # 内容
                    "msgId": "11234567890123456789012345678901"  # 32位随机字符串
                },
            "response": {
                "uri": "blockInfo",
                "body":
                    {
                        "type": "String",  # [b|r|s], 链类型
                        "chainKey": "String",  # 链编号
                        "nodeId": "String",  # 节点id
                        "height": "Number",  # 当前区块高度
                        "father": "String",  # 父区块hash
                        "hash": "String",  # 区块hash
                        "vrf": "String",  # VRF
                        "time": "Date",  # 当前产生时间
                        "interval": "Number",  # 出块间隔
                        "trans": "Number",  # 交易数量
                        "size": "Number",  # 区块大小
                        "detail":
                            {
                                "upStream": [{"key": "String", "hash": "String"}],  # 上传hash组
                                "downStream": [{"key": "String", "hash": "String"}],  # 下传hash组
                            }
                    },  # 单条数据
                "error": {"code": "", "message": ""},  # 错误
                "msgId": "11234567890123456789012345678901"  # 32位随机字符串
            },
        },
}
