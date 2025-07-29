# -*- coding: utf-8 -*-

"""
@Project : lqbox 
@File    : __init__.py.py
@Date    : 2025/2/8 9:47:09
@Author  : luke
@Desc    : 
"""

from requests import Response

from lqbox.base import BaseBox


class CanaryBox(BaseBox):
    base_url = 'aHR0cHM6Ly9mZWxsLXNlcnZlci1raXQubGVxZWUuY29t'

    def __init__(self):
        super().__init__(cookies={})

    def canary_request(self, api_path, body) -> Response:
        headers = {'content-type': 'application/json'}
        r = self.request(method="POST", url=f'{self.base_url}{api_path}', json=body, headers=headers)
        return r

    def exception_records(self, json_data):
        """查询"""
        # json_data = {
        #     'task_id': '',
        #     'start_time': '',
        #     'end_time': '',
        #     'category': [],
        #     'is_ok': '-1',
        #     'search_user': [],
        #     'search_shovel_name': '',
        #     'search_account_name': '',
        #     'search_level': [],
        # }
        return self.canary_request(api_path="/canary_api/exception_records", body=json_data)

    def mark_exception_records(self, json_data):
        """标记"""
        # json_data = {
        #     'send_data': [
        #         {
        #             'id': 0,
        #             'is_ok': True,
        #             'approval_time': None,
        #         },
        #     ],
        #     'comment': '',
        #     'account_user': '',
        # }
        return self.canary_request(api_path="/canary_api/exception_records/mark/handled", body=json_data)
