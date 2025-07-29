# -*- coding: utf-8 -*-

"""
@Project : lqbox 
@File    : __init__.py
@Date    : 2024/9/26 14:19:28
@Author  : luke
@Desc    : 
"""
import time

from requests import Response

from lqbox.base import BaseBox


class OpenCanaryBox(BaseBox):
    base_url = 'aHR0cHM6Ly9mZWxsLXNlcnZlci1raXQubGVxZWUuY29t'

    def __init__(self, tp_code, tp_secret):
        super().__init__(cookies={})
        self.tp_code = tp_code
        self.tp_secret = tp_secret

    def request_open_api(self, api_path, body) -> Response:
        noise = str(time.time() * 1000)
        headers = {
            'content-type': 'application/json',
            'noise': noise,
            'tp-code': self.tp_code,
            'sign': self.md5(f'{self.tp_code}&{noise}&{self.tp_secret}'),
        }
        r = self.request(method="POST", url=f'{self.base_url}{api_path}', json=body, headers=headers)
        return r

    def call_register_one_captcha_execution_record(self, captcha, status="SUCCESS", memo=None):
        data = {
            "captcha": captcha,
            "status": status,
        }
        if memo is not None:
            data['memo'] = memo
        return self.request_open_api(api_path="/open_api/register_one_captcha_execution_record", body=data)

    def call_get_captcha_execution_records(self, captcha, start_time, end_time):
        data = {
            "captcha": captcha,
            "start_time": start_time,
            "end_time": end_time,
        }
        return self.request_open_api(api_path="/open_api/get_captcha_execution_records", body=data)

    def call_register_one_fell_py_exception_record(self, data):
        return self.request_open_api(api_path="/open_api/register_one_py_exception_record", body=data)

    def call_get_fell_path_table_level(self, path_id):
        data = {"path_id": path_id}
        return self.request_open_api(api_path="/open_api/get_fell_path_table_level", body=data)


