# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : test
# @Date        : 2020/12/1 0001
# @Description : xjrw_chain_dashboard

import os
import logging
from . import common
from . import consts

level = 'debug'
LEVEL = dict(info=logging.INFO,
              warning=logging.WARNING,
              error=logging.ERROR,
              debug=logging.DEBUG,
              critical=logging.CRITICAL)
logging.basicConfig(level=LEVEL.get(level))
logger = logging.getLogger()


def create_log_file(log_file):
    path = os.path.dirname(log_file)
    if not os.path.isdir(path):
        os.makedirs(path)
    with open(log_file, mode='w', encoding='utf-8') as f:
        pass


def set_log_handler(level):
    if level == 'error':
        logger.addHandler(Log.log_file_handler_err)
    logger.addHandler(Log.log_file_handler)

def remove_log_handler(level):
    if level == 'error':
        logger.removeHandle(Log.log_file_handler_err)
    logger.removeHandler(Log.log_file_handler)



class Log(object):
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file = '%s/Log/%slog.log' % (path, common.current_time(consts.TIME_FORMAT_FILE))
    log_err_file = '%s/Log/%serr.log' % (path, common.current_time(consts.TIME_FORMAT_FILE))
    log_file_handler = logging.FileHandler(log_file, encoding='utf-8')
    log_file_handler_err = logging.FileHandler(log_err_file, encoding='utf-8')

    logger.setLevel(LEVEL.get(level))
    create_log_file(log_file)
    create_log_file(log_err_file)

    def __init__(self, type='log'):
        self.type = type

    def info(self, log_str):
        set_log_handler('info')
        s = "\n[%s][%s][INFO] %s" % (common.current_time(), self.type, log_str)
        logger.info(s)
        remove_log_handler('info')
        return s

    def warning(self, log_str):
        set_log_handler('warning')
        s = "[%s][%s][WARNING] %s" % (common.current_time(), self.type, log_str)
        logger.warning(s)
        remove_log_handler('warning')
        return s

    def error(self, log_str):
        set_log_handler('error')
        s = "[%s][%s][ERROR] %s" % (common.current_time(), self.type, log_str)
        logger.error(s)
        remove_log_handler('error')
        return s

    def debug(self, log_str):
        set_log_handler('debug')
        s = "[%s][%s][DEBUG] %s" % (common.current_time(), self.type, log_str)
        logger.debug(s)
        remove_log_handler('debug')
        return s

    def critical(self, log_str):
        set_log_handler('critical')
        s = "[%s][%s][CRITICAL] %s" % (common.current_time(), self.type, log_str)
        logger.critical(s)
        remove_log_handler('critical')
        return s


if __name__ == '__main__':
    Log.info("test info")
    Log.warning("test warning")
    Log.error("test error")
    Log.debug("test debug")
    Log.critical("test critical")

