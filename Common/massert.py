# -*- coding:utf-8 -*-
# @Author      : FangChao
# @File        : assert2
# @Date        : 2020/12/2 0002
# @Description : xjrw_chain_dashboard

import json
from Common import log
from Common import common

class Assertions(object):
    def __init__(self):
        self.log = log.Log('assert')

    def assert_code(self, code, expected_code):
        """
        check response status code
        """
        try:
            assert code == expected_code
            self.log.info("Case Assert success: expected_code is: %s, statusCode is: %s " % (expected_code, code))
            return True
        except:
            self.log.error("Case Assert failed: statusCode error, expected_code is: %s, statusCode is: %s " % (expected_code, code))
            raise

    def assert_body(self, body, body_msg, expected_msg):
        """
        check a property value in response body
        """
        try:
            msg = body[body_msg]
            assert msg == expected_msg
            self.log.info("Case Assert success: Response body msg == expected_msg, expected_msg is: %s, body_msg is: %s" %
                           (expected_msg, msg))
            return True
        except:
            self.log.error("Case Assert failed: Response body msg != expected_msg, expected_msg is: %s, body_msg is: %s" %
                           (expected_msg, msg))
            raise

    def assert_body_code_ge(self, body, ge_code):
        """
        check a property value in response body
        """
        try:
            body_code = body['code']
            assert body_code >= ge_code
            self.log.info("Case Assert success : Response body code %s >= %s" % (body_code, ge_code))
            return True
        except:
            self.log.error("Case Assert : Response body code < ge_code, expected_code must >= %s, body_code is: %s" %
                           (ge_code, body_code))
            raise

    def assert_in_text(self, body, expected_msg):
        """
        check expected message in response body
        """
        try:
            text = json.dumps(body, ensure_ascii=False)
            # print(text)
            assert expected_msg in text
            return True
        except:
            self.log.error("Case Assert : Response body Does not contain expected_msg, expected_msg is: %s" %
                           expected_msg)
            raise

    def assert_text(self, body, expected_msg):
        """
        check if response body is expected message
        """
        try:
            assert body == expected_msg
            self.log.info("Case Assert success: Response text == expected_msg, text is: %s, expected_msg is: %s " %
                           (body, expected_msg))
            return True

        except:
            self.log.error("Case Assert failed: Response text != expected_msg, text is: %s , expected_msg is: %s " %
                           (body, expected_msg))
            raise



    def assert_time(self, time, expected_time):
        """
        check if response time of body less than expected time. (ms)
        """
        try:
            assert time < expected_time
            self.log.info("Case Assert success : Response time %s < %s" % (time, expected_time))
            return True
        except:
            self.log.error("Case Assert : Response time >= expected_time, expected_time is: %s, time is: %s" %
                           (expected_time, time))
            raise

    def assert_db_text(self, db_text, expected_msg):
        """
        check if database text is expected message
        """
        try:
            assert expected_msg == db_text
            self.log.info("Case Assert success: db_text == expected_msg, expected_msg is: %s, db_text is: %s" %
                          (expected_msg, db_text))
            return True

        except:
            self.log.error("Case Assert failed: db_text != expected_msg, expected_msg is: %s, db_text is: %s" %
                           (expected_msg, db_text))
            raise

    def assert_db_counts(self, db_content, expected_counts):
        """
        check if database text is expected message
        """
        try:
            db_counts = len(db_content)
            assert len(db_content) == expected_counts
            self.log.info("Case Assert success: db_counts == expected_counts, expected_counts is: %s, db_counts is: %s" %
                          (expected_counts, db_counts))
            return True

        except:
            self.log.error("Case Assert failed: db_counts != expected_counts, expected_counts is: %s, db_counts is: %s" %
                           (expected_counts, db_counts))
            raise

    def assert_key_not_exist(self, m_dict, expected_key):
        """
        check if a dict do not have a unexpected key
        """
        try:
            assert common.dict_key_not_exist(m_dict, expected_key)
            self.log.info(f"Case Assert success: {m_dict} do not has key {expected_key}")
            return True

        except:
            self.log.error(f"Case Assert failed: {m_dict} has key {expected_key}")
            raise

    def assert_key_exist(self, m_dict, expected_key):
        """
        check if a dict have a expected key
        """
        try:
            assert common.dict_key_exist(m_dict, expected_key)
            self.log.info(f"Case Assert success: {m_dict} has key {expected_key}")
            return True

        except:
            self.log.error(f"Case Assert success: {m_dict} do not has key {expected_key}")
            raise

    def assert_value_not_None(self, m_dict):
        """
        check if a dict do not have a unexpected key
        """
        try:
            assert m_dict is not None
            self.log.info(f"Case Assert success: check value [{m_dict}] is not None")
            return True

        except:
            self.log.error(f"Case Assert failed: check value {m_dict} is None")
            raise