# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : templates.py
# @Date        : 2020/12/12 0012
# @Description : xjrw_chain_dashboard

header = {"Content-Type": "application/json",
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/85.0.4183.102 Safari/537.36',
           'Connection':'close'}

block_post_data = {
    "type": "B|R|S",  # input value
    "chainKey": "FF|FFFF",  # input value
    "nodeId": "",  # input value
    "height": 0,  # generated dynamically
    "father": "",  # generated dynamically
    "hash": "",  # generated dynamically
    "gas": "gas",  # static value
    "vrf": "vrf",  # static value
    "time": "",  # generated dynamically
    "interval": 0,  # generated dynamically
    "trans": 9,  # generated dynamically
    "size": 0,  # generated dynamically
    "lockHash": [{"type": "S", "chainkey": "0101", "height": 1}],  # generated dynamically
    "upHash": "HRfromRa",  # R|S: generated dynamically;  B: None
    "downHash": "HBtoRa",  # B|R: generated dynamically;  S: None
    "detail": {
        "upStream": [{"fromkey": "R01", "tokey": "R02", "hash": "HR01toS0201"},  # S: generated dynamically
                     {"fromkey": "R01", "tokey": "R03", "hash": "HR01toS0301"}],  # R: static value;  B: None
        "downStream": [
            {"fromkey": "R02", "tokey": "S0103", "hash": "HRbtoSa3"},  # B|R: static value
            {"fromkey": "R03", "tokey": "S0102", "hash": "HRctoSa2"},  # S: None
            {"fromkey": "R01", "tokey": "S0101", "hash": "HRatoSa1"}],
        "ss": []
    }
}
