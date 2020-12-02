# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : cmd
# @Date        : 2020/12/1
# @Description : xjrw_chain_dashboard

import subprocess


class Cmd:
    @staticmethod
    def run(cmd):
        output, errors = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return output.decode("utf-8")
