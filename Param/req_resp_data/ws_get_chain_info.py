# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : ws_get_chain_info
# @Date        : 2020/12/5 0005
# @Description : xjrw_chain_dashboard


# WEBSOCKET_API_GET_CHAIN_INFO request data and response data
data = {
    "url": "ws://192.168.0.164:9999/v1.0/conn",
    # for case: get_chain_info
    "get_chain_info":
        {
            "request": {
                "uri": "chainInfo",  # 命令地址
                "body": {},  # 内容
                "msgId": "01234567890123456789012345678901"  # 32位随机字符串
            },
            "response":
                {
                    "uri": "chainInfo",
                    "body":
                        {
                            "data": [{
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
                            }]
                        },
                    "error": {"code": "", "message": ""},  # 错误
                    "msgId": "01234567890123456789012345678901"  # 32位随机字符串
                },
        },

    # for case: get_chain_info_update_data
    "get_chain_info_update_data":
        {
            "request": {
                "uri": "chainInfo",  # 命令地址
                "body": {},  # 内容
                "msgId": "01234567890123456789012345678901"  # 32位随机字符串
            },
            "response":
                {
                    "uri": "chainInfo",
                    "body":
                        {
                            "data": [{
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
                            }]
                        },
                    "error": {"code": "", "message": ""},  # 错误
                    "msgId": "01234567890123456789012345678901"  # 32位随机字符串
                },
        },

    # for case: get_chain_info_insert_data
    "get_chain_info_insert_data":
        {
            "request": {
                "uri": "chainInfo",  # 命令地址
                "body": {},  # 内容
                "msgId": "01234567890123456789012345678901"  # 32位随机字符串 # "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxx"
            },
            "response":
                {
                    "uri": "chainInfo",
                    "body":
                        {
                            "data": [{
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
                            }]
                        },
                    "error": {"code": "", "message": ""},  # 错误
                    "msgId": "01234567890123456789012345678901"  # 32位随机字符串
                },
        },
}
