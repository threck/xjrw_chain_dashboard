# API_Automation_Test

## need to install some libraries:
>pip3 install pytest pytest-html allure-pytest pymongo requests requests-toolbelt websocket-client base58 pytz

>pip3 install websockets asyncio

## configuration:
config:
Stress/Conf/config.py

CHAIN_NU_TOTAL = {"R": 2, "S": 4} -- set R|S total chain number:

CHAIN_NU_LOCAL = {"R": 2, "S": 4} -- set R|S chain number on a client environment:

SS_TRADE_NU = 3 -- set trans number on each shard-key:

STRESS_LOOP_TIME = 0 -- set loop time of each stress test ( B -> R -> S )
##### if you want loop [n] time, you should set the value to [n+1]
##### if you want to run forever, you should set the value to 0

STRESS_LOOP_INTERVAL = 2 -- set the loop interval time between every B->R->S post send cycle.


## how to run:
> source /home/venv**/bin/activate

> bash start_server.sh  # start ws server

> bash start_client.sh n  # start ws client. n is client number


