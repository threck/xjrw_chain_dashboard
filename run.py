# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : test
# @Date        : 2020/12/1 0001
# @Description : xjrw_chain_dashboard
"""
run testcase：
    python run.py
"""

import os
import pytest
from Common import log
from Common import common
from Common import consts
from Config import config
from Common import memail
from Common import cmd as command

if __name__ == '__main__':
    # initial
    log = log.Log()
    config = config.Config()
    log.info('initialize the configuration file, path: %s' % config.conf_path)
    xml_report_path = config.xml_report_path
    html_report_path = config.html_report_path
    xml_report_path_allure = os.path.join(config.xml_report_path,
                                          'allure%s' % common.current_time(consts.TIME_FORMAT_FILE))
    html_report_path_allure = os.path.join(config.html_report_path,
                                           'allure%s' % common.current_time(consts.TIME_FORMAT_FILE))

    # run pytest
    # /test_httpapi.py::TestHTTPAPITest::test_heart_beat_update_data
    # /test_wsapi.py::TestWSAPITest::test_get_real_chain_block_info_with_sub
    # -m http  # run testcases which marked as http
    args_allure = ['-s', '-q', '--alluredir', xml_report_path_allure,
                   'Testcase/test_wsapi.py::TestWSAPITest::test_get_real_chain_block_info_with_sub']
    args_pytest = ['-s', '-v', '--html=%s' % os.path.join(html_report_path,
                                                          'pytest-html%s' % common.current_time(consts.TIME_FORMAT_FILE),
                                                          'report.html'),
                   'Testcase/test_httpapi.py']
    pytest.main(args_allure)

    # generate allure html reports
    cmd = 'allure generate %s -o %s' % (xml_report_path_allure, html_report_path_allure)
    try:
        command = command.Cmd()
        command.run(cmd)
    except Exception:
        log.error('testcase failed to run, check environment configuration please!')
        raise

    # # send email
    # try:
    #     # email configuration
    #     qq_mail = memail.Email()
    #     qq_mail.smtp_server = config.smtpserver_email
    #     qq_mail.smtp_server_port = config.smtpserverport_email
    #     qq_mail.from_addr = config.from_email
    #     qq_mail.username = config.username_email
    #     qq_mail.to_addr = config.to_email
    #     qq_mail.password = config.password_email
    #     # do send
    #     msg = qq_mail.set_msg()
    #     qq_mail.login()
    #     qq_mail.send(msg)
    #     qq_mail.logout()
    # except Exception as e:
    #     log.error('send email failed, check email config please!')
    #     raise
