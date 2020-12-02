# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : test
# @Date        : 2020/12/1 0001
# @Description : xjrw_chain_dashboard
"""
run testcase：
    python run.py
# '--allure_severities=critical, blocker'
# '--allure_stories=测试模块_demo1, 测试模块_demo2'
# '--allure_features=测试features'
"""

import pytest
from Common import log
from Config import config
from Common import email
from Common import cmd as command

if __name__ == '__main__':
    # initial
    log = log.Log()
    config = config.Config()
    log.info('initialize the configuration file, path:' + config.conf_path)
    xml_report_path = config.xml_report_path
    html_report_path = config.html_report_path

    # run pytest
    args = ['-s', '-q', '--alluredir', xml_report_path]
    pytest.main(args)

    # generate allure html reports
    cmd = 'allure generate %s -o %s' % (xml_report_path, html_report_path)
    try:
        command = command.Cmd()
        command.run(cmd)
    except Exception:
        log.error('testcase failed to run, check environment configuration please!')
        raise

    # send email
    try:
        # email configuration
        qq_mail = email.Email()
        qq_mail.smtp_server = config.smtpserver_email
        qq_mail.smtp_server_port = config.smtpserverport_email
        qq_mail.from_addr = config.from_email
        qq_mail.username = config.username_email
        qq_mail.to_addr = config.to_email
        qq_mail.password = config.password_email
        # do send
        msg = qq_mail.set_msg()
        qq_mail.login()
        qq_mail.send(msg)
        qq_mail.logout()
    except Exception as e:
        log.error('send email failed, check email config please!')
        raise
