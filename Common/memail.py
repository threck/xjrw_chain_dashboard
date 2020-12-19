# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : email.py
# @Date        : 2020/12/1
# @Description : python3

import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
from email.header import Header
from Config import config

class Email(object):
    def __init__(self):
        self.__smtp_server = None
        self.__smtp_server_port = None
        self.__from_addr = None
        self.__to_addr = None
        self.__username = None
        self.__password = None
        self.__server = None

    @property
    def smtp_server(self):
        return self.__smtp_server

    @smtp_server.setter
    def smtp_server(self, value):
        self.__smtp_server = value

    @property
    def smtp_server_port(self):
        return self.__smtp_server_port

    @smtp_server_port.setter
    def smtp_server_port(self, value):
        if not isinstance(value, int):
            raise TypeError('smtp_server_port must be int! ')
        self.__smtp_server_port = value

    @property
    def from_addr(self):
        return self.__from_addr

    @from_addr.setter
    def from_addr(self, value):
        self.__from_addr = value

    @property
    def to_addr(self):
        return self.__to_addr

    @to_addr.setter
    def to_addr(self, value):
        if not isinstance(value, list):
            raise TypeError("to_addr must be a list! like : ['***@***.com', '***@***.com']")
        self.__to_addr = value

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        self.__username = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        self.__password = value

    def login(self):
        self.__server = smtplib.SMTP_SSL(self.__smtp_server, self.__smtp_server_port)
        self.__server.set_debuglevel(1)  # 用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息
        self.__server.login(self.__username, self.__password)

    def send(self, msg):
        # 邮件正文是一个str，as_string()把MIMEText对象变成str
        self.__server.sendmail(self.__from_addr, self.__to_addr, msg.as_string())

    def logout(self):
        self.__server.quit()

    def set_msg(self):
        msg = MIMEMultipart('alternative')
        msg['From'] = self._format_addr('Python developer <%s>' % self.__from_addr)
        msg['To'] = self._format_addr('administrator <%s>' % ','.join(self.__to_addr))
        msg['Subject'] = Header('A test python email', 'utf-8').encode()

        # 邮件正文
        msg_plain = MIMEText('api test email', 'plain', 'utf-8')

        msg.attach(msg_plain)
        return msg

    # 函数_format_addr()格式化一个邮件地址。注意不能简单地传入name <addr@example.com>，因为如果包含中文，需要通过Header对象进行编码
    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

