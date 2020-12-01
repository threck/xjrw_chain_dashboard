# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : test
# @Date        : 2020/12/1 0001
# @Description : xjrw_chain_dashboard

import os
import logging
import time

level = 'info'
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


class Log(object):
    time_format = '%Y-%m-%d %H:%M:%S'

    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file = path + '/Log/log.log'
    log_err_file = path + '/Log/err.log'
    log_file_handler = logging.FileHandler(log_file, encoding='utf-8')
    log_file_handler_err = logging.FileHandler(log_err_file, encoding='utf-8')

    logger.setLevel(LEVEL.get(level))
    create_log_file(log_file)
    create_log_file(log_err_file)

    @staticmethod
    def set_log_handler(level):
        if level == 'error':
            logger.addHandler(Log.log_file_handler_err)
        logger.addHandler(Log.log_file_handler)

    @staticmethod
    def remove_log_handler(level):
        if level == 'error':
            logger.removeHandler(Log.log_file_handler_err)
        logger.removeHandler(Log.log_file_handler)

    @staticmethod
    def current_time():
        return time.strftime(Log.time_format, time.localtime())

    @staticmethod
    def info(log_str):
        Log.set_log_handler('info')
        logger.info("["+Log.current_time()+"][INFO] "+log_str)
        Log.remove_log_handler('info')

    @staticmethod
    def warning(log_str):
        Log.set_log_handler('warning')
        logger.warning("["+Log.current_time()+"][WARNING] "+log_str)
        Log.remove_log_handler('warning')

    @staticmethod
    def error(log_str):
        Log.set_log_handler('error')
        logger.error("["+Log.current_time()+"][ERROR] "+log_str)
        Log.remove_log_handler('error')

    @staticmethod
    def debug(log_str):
        Log.set_log_handler('debug')
        logger.debug("["+Log.current_time()+"][DEBUG] "+log_str)
        Log.remove_log_handler('debug')

    @staticmethod
    def critical(log_str):
        Log.set_log_handler('critical')
        logger.critical("["+Log.current_time()+"][CRITICAL] "+log_str)
        Log.remove_log_handler('critical')


if __name__ == '__main__':
    Log.info("test info")
    Log.warning("test warning")
    Log.error("test error")
    Log.debug("test debug")
    Log.critical("test critical")

