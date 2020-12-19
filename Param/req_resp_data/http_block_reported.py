# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : http_block_reported
# @Date        : 2020/12/5 0005
# @Description : xjrw_chain_dashboard

# HTTP_API_BLOCK_REPORTED request data and response data
data = {
    "url": "/api/v1.0/block",
    "header": {"Content-Type": "application/json",
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/85.0.4183.102 Safari/537.36'},

    # for case: block_reported_shard_chain
    "block_reported_shard_chain":
        {
            "request":
                {
                    "type": "S",
                    "chainKey": "0101",
                    "nodeId": "12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBqs01",
                    "height": 1,
                    "father": "0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a12f4217b0000",
                    "hash": "0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a12f4217b0100",
                    "gas": "gas",
                    "vrf": "vrf",
                    "time": "2020-12-08T16:03:04.872160+08:00",
                    "interval": 1,
                    "trans": 9,
                    "size": 1,
                    "lockHash": [{"type": "R", "chainkey": "01", "height": 1}],
                    "upHash": "HSfromS0101",
                    "downHash": "",
                    "detail": {
                        "upStream": [{"fromkey": "S0101", "tokey": "R01", "hash": "HS0101_S0102"},
                                     {"fromkey": "S0101", "tokey": "R01", "hash": "HS0101_S0103"},
                                     {"fromkey": "S0101", "tokey": "R02", "hash": "HS0101_S0201"},
                                     {"fromkey": "S0101", "tokey": "R02", "hash": "HS0101_S0203"},
                                     {"fromkey": "S0101", "tokey": "R03", "hash": "HS0101_S0301"},
                                     {"fromkey": "S0101", "tokey": "R03", "hash": "HS0101_S0302"},
                                     {"fromkey": "S0101", "tokey": "R03", "hash": "HS0101_S0303"}
                                     ],
                        "downStream": [],
                        "ss":
                            [
                                {"fromShard": "S0101",
                                 "toShard": "S0102",
                                 "fromRelay": "R01",
                                 "toRelay": "R01",
                                 "hash": "0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a12f4217bss01",
                                 "trans": [
                                     {"hash": "0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a1ss01trans01",
                                      "from": "wallet_S0101_1", "to": "wallet_S0102_1", "amount": 3},
                                     {"hash": "0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a1ss01trans02",
                                      "from": "wallet_S0101_1", "to": "wallet_S0102_2", "amount": 3}
                                 ]},
                                {"fromShard": "S0101",
                                 "toShard": "S0201",
                                 "fromRelay": "R01",
                                 "toRelay": "R02",
                                 "hash": "0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a12f4217bss02",
                                 "trans": [
                                     {"hash": "0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a1ss02trans01",
                                      "from": "wallet_S0101_1", "to": "wallet_S0201_1", "amount": 3},
                                     {"hash": "0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a1ss02trans02",
                                      "from": "wallet_S0101_1", "to": "wallet_S0201_2", "amount": 3}
                                 ]},
                                {"fromShard": "S0101",
                                 "toShard": "S0301",
                                 "fromRelay": "R01",
                                 "toRelay": "R03",
                                 "hash": "0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a12f4217bss03",
                                 "trans": [
                                     {"hash": "0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a1ss03trans01",
                                      "from": "wallet_S0101_1", "to": "wallet_S0301_1", "amount": 3},
                                     {"hash": "0x9fe109fec8b1751e4fae65e2bbaa6a31c580bac257436c43800a1ss03trans02",
                                      "from": "wallet_S0101_1", "to": "wallet_S0301_2", "amount": 3}
                                 ]}
                            ]
                    }
                },
            "response": {
                "code": 200,
                "message": "OK",
                "data": {},
            },
        },

    # for case: block_reported_relay_chain
    "block_reported_relay_chain":
        {
            "request":
                {
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
                    "upHash": "HRfromRa",
                    "downHash": "HBtoRa",
                    "detail": {
                        "upStream": [{"fromkey": "R01", "tokey": "S0201", "hash": "HRatoSb1"},
                                     {"fromkey": "R01", "tokey": "S0301", "hash": "HRatoSc1"}
                                     ],
                        "downStream": [
                                       {"fromkey": "R02", "tokey": "S0103", "hash": "HRbtoSa3"},
                                       {"fromkey": "R03", "tokey": "S0102", "hash": "HRctoSa2"},
                                       {"fromkey": "R01", "tokey": "S0101", "hash": "HRatoSa1"}
                                       ]
                    }
                },
            "response": {
                "code": 200,
                "message": "OK",
                "data": {},
            },
        },

    # for case: block_reported_beacon_chain
    "block_reported_beacon_chain":
        {
            "request":
                {
                    "type": "B",
                    "chainKey": "B",
                    "nodeId": "12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBqb01",
                    "height": 1,
                    "father": "father",
                    "hash": "bolock_hash_b_0",
                    "gas": "gas",
                    "vrf": "vrf",
                    "time": "2020-12-08T16:03:04.872160+08:00",
                    "interval": 1,
                    "trans": 9,
                    "size": 1,
                    "lockHash": [{"type": "R", "chainkey": "01", "height": 1}],
                    "upHash": "",
                    "downHash": "HB",
                    "detail": {
                        "upStream": [],
                        "downStream": [{"fromkey": "B", "tokey": "R01", "hash": "HBtoR01"},
                                       {"fromkey": "B", "tokey": "R02", "hash": "HBtoR02"},
                                       {"fromkey": "B", "tokey": "R03", "hash": "HBtoR03"}]
                    }
                },
            "response": {
                "code": 200,
                "message": "OK",
                "data": {},
            },
        },

    # for case: block_reported_duplicated_data
    "block_reported_duplicated_data":
        {
            "request":
                {
                    "type": "R",
                    "chainKey": "01",
                    "nodeId": "12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBqr01",
                    "height": 1,
                    "father": "father",
                    "hash": "bolock_hash_Ra_0",
                    "gas": "gas",
                    "vrf": "vrf",
                    "time": "2014-03-25T06:26:01.927+08:00",
                    "interval": 1,
                    "trans": 9,
                    "size": 1,
                    "lockHash": [{"type": "S", "chainkey": "0101", "height": 1}],
                    "upHash": "HRfromRa",
                    "downHash": "HBtoRa",
                    "detail": {
                        "upStream": [{"fromkey": "Ra", "tokey": "Sb1", "hash": "HRatoSb1"},
                                     {"fromkey": "Ra", "tokey": "Sb2", "hash": "HRatoSb2"},
                                     {"fromkey": "Ra", "tokey": "Sb3", "hash": "HRatoSb3"},
                                     {"fromkey": "Ra", "tokey": "Sc1", "hash": "HRatoSc1"},
                                     {"fromkey": "Ra", "tokey": "Sc2", "hash": "HRatoSc2"},
                                     {"fromkey": "Ra", "tokey": "Sc3", "hash": "HRatoSc3"}
                                     ],
                        "downStream": [{"fromkey": "Rb", "tokey": "Sa1", "hash": "HRbtoSa1"},
                                       {"fromkey": "Rb", "tokey": "Sa2", "hash": "HRbtoSa2"},
                                       {"fromkey": "Rb", "tokey": "Sa3", "hash": "HRbtoSa3"},
                                       {"fromkey": "Rc", "tokey": "Sa1", "hash": "HRctoSa1"},
                                       {"fromkey": "Rc", "tokey": "Sa2", "hash": "HRctoSa2"},
                                       {"fromkey": "Rc", "tokey": "Sa3", "hash": "HRctoSa3"},
                                       {"fromkey": "Ra", "tokey": "Sa1", "hash": "HRatoSa1"},
                                       {"fromkey": "Ra", "tokey": "Sa2", "hash": "HRatoSa2"},
                                       {"fromkey": "Ra", "tokey": "Sa3", "hash": "HRatoSa3"}
                                       ]
                    }
                },
            "response": {
                "code": 200,
                "message": "OK",
                "data": {}
            }
        },

    # for case: block_reported_update_data
    "block_reported_update_data":
        {
            "request":
                [{"type": "R",
                  "chainKey": "01",
                  "nodeId": "12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBqr01",
                  "height": 1,
                  "father": "father",
                  "hash": "bolock_hash_Ra_0",
                  "gas": "gas",
                  "vrf": "vrf",
                  "time": "2020-12-08T16:03:04.872160+08:00",
                  "interval": 1,
                  "trans": 9,
                  "size": 1,
                  "lockHash": [{"type": "S", "chainkey": "0101", "height": 1}],
                  "upHash": "HRfromRa",
                  "downHash": "HBtoRa",
                  "detail":
                      {
                          "upStream": [{"fromkey": "R01", "tokey": "Sb1", "hash": "HRatoSb1"},
                                       {"fromkey": "Ra", "tokey": "Sb2", "hash": "HRatoSb2"},
                                       {"fromkey": "Ra", "tokey": "Sb3", "hash": "HRatoSb3"},
                                       {"fromkey": "Ra", "tokey": "Sc1", "hash": "HRatoSc1"},
                                       {"fromkey": "Ra", "tokey": "Sc2", "hash": "HRatoSc2"},
                                       {"fromkey": "Ra", "tokey": "Sc3", "hash": "HRatoSc3"}
                                       ],
                          "downStream": [{"fromkey": "Rb", "tokey": "Sa1", "hash": "HRbtoSa1"},
                                         {"fromkey": "Rb", "tokey": "Sa2", "hash": "HRbtoSa2"},
                                         {"fromkey": "Rb", "tokey": "Sa3", "hash": "HRbtoSa3"},
                                         {"fromkey": "Rc", "tokey": "Sa1", "hash": "HRctoSa1"},
                                         {"fromkey": "Rc", "tokey": "Sa2", "hash": "HRctoSa2"},
                                         {"fromkey": "Rc", "tokey": "Sa3", "hash": "HRctoSa3"},
                                         {"fromkey": "Ra", "tokey": "Sa1", "hash": "HRatoSa1"},
                                         {"fromkey": "Ra", "tokey": "Sa2", "hash": "HRatoSa2"},
                                         {"fromkey": "Ra", "tokey": "Sa3", "hash": "HRatoSa3"}
                                         ]
                      }
                  }, {
                     "type": "R",
                     "chainKey": "01",
                     "nodeId": "12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBqr02",
                     "height": 1,
                     "father": "father",
                     "hash": "bolock_hash_Ra_0",
                    "gas": "gas",
                     "vrf": "vrf",
                     "time": "2014-03-25T06:26:01.927+08:00",
                     "interval": 1,
                     "trans": 9,
                     "size": 1,
                     "lockHash": [{"type": "S", "chainkey": "0201", "height": 1}],
                     "upHash": "HRfromRa11111111",
                     "downHash": "HBtoRa111111111",
                     "detail": {
                         "upStream": [{"fromkey": "Ra", "tokey": "Sb1", "hash": "HRatoSb1"},
                                      {"fromkey": "Ra", "tokey": "Sb2", "hash": "HRatoSb2"},
                                      {"fromkey": "Ra", "tokey": "Sb3", "hash": "HRatoSb3"},
                                      {"fromkey": "Ra", "tokey": "Sc1", "hash": "HRatoSc1"},
                                      {"fromkey": "Ra", "tokey": "Sc2", "hash": "HRatoSc2"},
                                      {"fromkey": "Ra", "tokey": "Sc3", "hash": "HRatoSc3"}
                                      ],
                         "downStream": [{"fromkey": "Rb", "tokey": "Sa1", "hash": "HRbtoSa1"},
                                        {"fromkey": "Rb", "tokey": "Sa2", "hash": "HRbtoSa2"},
                                        {"fromkey": "Rb", "tokey": "Sa3", "hash": "HRbtoSa3"},
                                        {"fromkey": "Rc", "tokey": "Sa1", "hash": "HRctoSa1"},
                                        {"fromkey": "Rc", "tokey": "Sa2", "hash": "HRctoSa2"},
                                        {"fromkey": "Rc", "tokey": "Sa3", "hash": "HRctoSa3"},
                                        {"fromkey": "Ra", "tokey": "Sa1", "hash": "HRatoSa1"},
                                        {"fromkey": "Ra", "tokey": "Sa2", "hash": "HRatoSa2"},
                                        {"fromkey": "Ra", "tokey": "Sa3", "hash": "HRatoSa3"}
                                        ]
                     }
                 }],
            "response": {
                "code": 200,
                "message": "OK",
                "data": {},
            },
        },

    # for case: block_reported_wrong_value_chain_type
    "block_reported_wrong_value_chain_type":
        {
            "request": {
                "type": "A",
                "chainKey": "01",
                "nodeId": "12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBqr01",
                "height": 1,
                "father": "father",
                "hash": "bolock_hash_Ra_0",
                "gas": "gas",
                "vrf": "vrf",
                "time": "2020-12-08T16:03:04.872160+08:00",
                "interval": 1,
                "trans": 9,
                "size": 1,
                "lockHash": [{"type": "S", "chainkey": "0101", "height": 1}],
                "upHash": "HRfromRa",
                "downHash": "HBtoRa",
                "detail": {
                    "upStream": [{"fromkey": "Ra", "tokey": "Sb1", "hash": "HRatoSb1"},
                                 {"fromkey": "Ra", "tokey": "Sb2", "hash": "HRatoSb2"}],
                    "downStream": [{"fromkey": "Rb", "tokey": "Sa1", "hash": "HRbtoSa1"},
                                   {"fromkey": "Rb", "tokey": "Sa2", "hash": "HRbtoSa2"},
                                   {"fromkey": "Rb", "tokey": "Sa3", "hash": "HRbtoSa3"}]
                },
            },
            "response": {
                "code": 400,
                "message": "error",
                "data": {},
            },
        },

    # for case: block_reported_null_value_chain_type
    "block_reported_null_value_chain_type":
        {
            "request": {
                "type": "",
                "chainKey": "01",
                "nodeId": "12D3KooWGKa86zkRz11uFp7kja4FujbQYnTt7qZQQMGfoBfBqr01",
                "height": 1,
                "father": "father",
                "hash": "bolock_hash_Ra_0",
                "gas": "gas",
                "vrf": "vrf",
                "time": "2020-12-08T16:03:04.872160+08:00",
                "interval": 1,
                "trans": 9,
                "size": 1,
                "lockHash": [{"type": "S", "chainkey": "0101", "height": 1}],
                "upHash": "HRfromRa",
                "downHash": "HBtoRa",
                "detail": {
                    "upStream": [{"fromkey": "Ra", "tokey": "Sb1", "hash": "HRatoSb1"},
                                 {"fromkey": "Ra", "tokey": "Sb2", "hash": "HRatoSb2"}],
                    "downStream": [{"fromkey": "Rb", "tokey": "Sa1", "hash": "HRbtoSa1"},
                                   {"fromkey": "Rb", "tokey": "Sa2", "hash": "HRbtoSa2"},
                                   {"fromkey": "Rb", "tokey": "Sa3", "hash": "HRbtoSa3"}]
                },
            },
            "response": {
                "code": 400,
                "message": "error",
                "data": {},
            },
        },
}
