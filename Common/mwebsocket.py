# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : mwebsockets
# @Date        : 2020/12/2 0002
# @Description : xjrw_chain_dashboard

import websocket
import time
import json
import requests
from Common import log

class WebSocket(object):
    def __init__(self, url):
        self.log = log.Log()
        if not url.startswith('ws://'):
            self.url = '%s%s' % ('ws://', url)
        self.url = url
        self.log.info(f'websocket addr: {self.url}')
        self.ws = websocket.create_connection(self.url)

    def send(self, data):
        """
        WebSocket Send Request
        """
        try:
            if data is None:
                self.ws.send()
            else:
                self.log.info(f'websocket send msg: {json.dumps(data)}')
                self.ws.send(json.dumps(data))
            return
        except websocket.WebSocketException as e:
            print('%s%s' % ('WebSocketException url: ', self.url))
            print(e)
            return

        except Exception as e:
            print('%s%s' % ('Exception url: ', self.url))
            print(e)
            return

    def receive(self):
        """
        WebSocket Receive Response
        """
        try:
            response = self.ws.recv()
            self.log.info(f'websocket recv msg: {response}')

        except websocket.WebSocketException as e:
            self.log.info('%s%s' % ('WebSocketException url: ', self.url))
            return dict()
        except Exception as e:
            self.log.info('%s%s' % ('Exception url: ', self.url))
            return dict()
        try:
            response = json.loads(response)
        except websocket.WebSocketException as e:
            self.log.info('%s%s' % ('WebSocketException recv: ', e))
            return dict()
        return response
