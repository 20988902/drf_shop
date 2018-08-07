#!/usr/bin/env python
#coding: utf-8
__author__ = 'lixl'
__date__ = '2018/7/26 21:49'

import requests
import json

class YunPian:
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.cn/single_send.js"

    def send_sms(self, code, mobile):
        params = {
            'apikey': self.api_key,
            'mobile': mobile,
            'text': '您的验证码是{code}'.format(code=code)
        }

        response = requests.post(self.single_send_url, data=params)

        re_dict = json.loads(response.text)
        return re_dict

