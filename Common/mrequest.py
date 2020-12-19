# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : test
# @Date        : 2020/12/1 0001
# @Description : xjrw_chain_dashboard

import os
import random
import requests
import json
from Common import consts
from Common import log
from requests_toolbelt import MultipartEncoder


class Request(object):

    def get_request(self, url, data, header):
        """
        Get Request
        """
        if not url.startswith('http://'):
            url = '%s%s' % ('http://', url)
            print(url)

        try:
            log.Log().info(f'get request api_url: {url}')
            log.Log().info(f'get request params: {data}')
            log.Log().info(f'get request header: {header}')
            if data is None:
                response = requests.get(url=url, headers=header)
            else:
                response = requests.get(url=url, params=data, headers=header)

        except requests.RequestException as e:
            print('%s%s' % ('RequestException url: ', url))
            print(e)
            return ()

        except Exception as e:
            print('%s%s' % ('Exception url: ', url))
            print(e)
            return ()
        # get api response time
        time_consuming = response.elapsed.microseconds/1000
        time_total = response.elapsed.total_seconds()

        response_dicts = dict()
        response_dicts['code'] = response.status_code
        try:
            response_dicts['body'] = response.json()
        except Exception as e:
            print(e)
            response_dicts['body'] = ''
        response_dicts['text'] = response.text
        response_dicts['time_consuming'] = time_consuming
        response_dicts['time_total'] = time_total

        return response_dicts

    def post_request(self, url, data, header):
        """
        Post Request
        """
        if not url.startswith('http://'):
            url = '%s%s' % ('http://', url)
        try:
            log.Log().info(f'post request api_url: {url}')
            log.Log().info(f'post request json data: {data}')
            log.Log().info(f'post request header: {header}')
            if data is None:
                response = requests.post(url=url, headers=header)
            else:
                response = requests.post(url=url, json=data, headers=header)
        except requests.RequestException as e:
            print('%s%s' % ('RequestException url: ', url))
            print(e)
            return ()

        except Exception as e:
            print('%s%s' % ('Exception url: ', url))
            print(e)
            return ()

        log.Log().info(f'post response text: {response.text}')
        time_consuming = response.elapsed.microseconds/1000
        time_total = response.elapsed.total_seconds()

        response_dicts = dict()
        response_dicts['code'] = response.status_code
        try:
            response_dicts['body'] = response.json()
        except Exception as e:
            print(e)
            response_dicts['body'] = ''

        response_dicts['text'] = response.text
        response_dicts['time_consuming'] = time_consuming
        response_dicts['time_total'] = time_total

        return response_dicts

    def post_request_multipart(self, url, data, header, file_parm, file, f_type):
        """
        Post Request with Multipart/form-data
        """
        if not url.startswith('http://'):
            url = '%s%s' % ('http://', url)
            print(url)
        try:
            if data is None:
                response = requests.post(url=url, headers=header)
            else:
                data[file_parm] = os.path.basename(file), open(file, 'rb'), f_type
                enc = MultipartEncoder(
                    fields=data,
                    boundary='--------------' + str(random.randint(1e28, 1e29 - 1))
                )

                header['Content-Type'] = enc.content_type
                response = requests.post(url=url, data=data, headers=header)

        except requests.RequestException as e:
            print('%s%s' % ('RequestException url: ', url))
            print(e)
            return ()

        except Exception as e:
            print('%s%s' % ('Exception url: ', url))
            print(e)
            return ()

        time_consuming = response.elapsed.microseconds/1000
        time_total = response.elapsed.total_seconds()

        response_dicts = dict()
        response_dicts['code'] = response.status_code
        try:
            response_dicts['body'] = response.json()
        except Exception as e:
            print(e)
            response_dicts['body'] = ''

        response_dicts['text'] = response.text
        response_dicts['time_consuming'] = time_consuming
        response_dicts['time_total'] = time_total

        return response_dicts

    def put_request(self, url, data, header):
        """
        Put Request
        """
        if not url.startswith('http://'):
            url = '%s%s' % ('http://', url)
            print(url)

        try:
            if data is None:
                response = requests.put(url=url, headers=header)
            else:
                response = requests.put(url=url, params=data, headers=header)

        except requests.RequestException as e:
            print('%s%s' % ('RequestException url: ', url))
            print(e)
            return ()

        except Exception as e:
            print('%s%s' % ('Exception url: ', url))
            print(e)
            return ()

        time_consuming = response.elapsed.microseconds/1000
        time_total = response.elapsed.total_seconds()

        response_dicts = dict()
        response_dicts['code'] = response.status_code
        try:
            response_dicts['body'] = response.json()
        except Exception as e:
            print(e)
            response_dicts['body'] = ''
        response_dicts['text'] = response.text
        response_dicts['time_consuming'] = time_consuming
        response_dicts['time_total'] = time_total

        return response_dicts