# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : __init__
# @Date        : 2020/12/1 0001
# @Description : xjrw_chain_dashboard

import pytest
import smtplib


# 当fixture超出范围时,通过使用yield语句而不是return,pytest支持fixture执行特定的teardown代码
# yield语句之后的所有代码都视为teardown代码
@pytest.fixture(scope="module")
def smtp_connection():
    smtp_connection = smtplib.SMTP("smtp.gmail.com", 587, timeout=5)
    yield smtp_connection  # provide the fixture value
    print("teardown smtp")
    smtp_connection.close()
    smtp_connection.close()


@pytest.fixture(scope='function')
def login_func(request):
    def teardown_function():
        print("teardown_function called.")

    request.addfinalizer(teardown_function)  # 此内嵌函数做teardown工作
    print("this is a [ function ] setup ...")


@pytest.fixture(scope='class')
def login_class(request):
    def teardown():
        print("this is a [ class ] teardown ...")
    request.addfinalizer(teardown)
    print("this is a [ class ] setup ...")


@pytest.fixture(scope='module')
def login_module():
    """firxture for module"""
    print("this is a [ module ] setup ...")


@pytest.fixture(scope='session')
def login_session():
    print("this is a [ session ] setup ...")


@pytest.fixture(scope="module",
                params=["smtp.gmail.com", "mail.python.org"])
def smtp_connection(request):
    smtp_connection = smtplib.SMTP(request.param, 587, timeout=5)
    yield smtp_connection
    print("finalizing %s" % smtp_connection)
    smtp_connection.close()
