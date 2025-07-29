# -*- coding: utf-8 -*-

"""
@Project : lqbox 
@File    : __init__.py.py
@Date    : 2024/2/4 10:03:54
@Author  : zhchen
@Desc    : 
"""
import re

import requests

from lqbox.base import BaseBox


class AliBox(BaseBox):

    def __init__(self, cookies):
        super().__init__(cookies)
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }
        self.get_csrf_token()

    def request(self, method, url, **kwargs):
        if kwargs.get('headers') is None:
            kwargs['headers'] = self.headers
        return super().request(method, url, **kwargs)

    def get_csrf_token(self):
        """获取csrf_token"""
        params = {
            'isShare': 'true',
            'hideTopbar': 'true',
            'readOnly': 'true',
            'hiddenQuickAnalysis': 'true',
            'hiddenLogReduce': 'true',
            'hiddenLogChart': 'true',
            'hiddenBack': 'true',
            'hiddenChangeProject': 'true',
            'hiddenOverview': 'true',
            'ignoreTabLocalStorage': 'true',
            'hiddenShare': 'true',
            'hiddenEtl': 'true',
            'hiddenProject': 'true',
            'hiddenReport': 'true',
            'hiddenTitleSetting': 'true',
        }

        response = self.request(
            url=f"{self.base_url}/lognext/project/octet/logsearch/elastic-oc",
            method="GET", params=params)
        csrf_token = re.findall(r'SEC_TOKEN: \"(.*)\"', response.text)[0]
        self.headers['X-Csrf-Token'] = str(csrf_token)


class AliLogBox(AliBox):
    base_url = "aHR0cHM6Ly9zbHM0c2VydmljZS5jb25zb2xlLmFsaXl1bi5jb20="

    @classmethod
    def login_from_mc(cls, url):
        session = requests.Session()
        response = session.get(url)
        cookies = dict(session.cookies)
        # print(cookies)
        return cls(cookies)

    def __ali_log_request(self, path, data):
        return self.request(url=f"{self.base_url}{path}", method="POST", data=data)

    def get_logs(self, data):
        """获取日志"""
        # data = {
        #     'ProjectName': '123',
        #     'LogStoreName': '123',
        #     'from': '1706976000',
        #     'query': 'exp | with_pack_meta',
        #     'to': '1707014768',
        #     'Page': '1',
        #     'Size': '20',
        #     'Reverse': 'true',
        #     'pSql': 'false',
        #     'schemaFree': 'false',
        #     'needHighlight': 'true',
        # }
        return self.__ali_log_request(path="/console/logs/getLogs.json", data=data)
