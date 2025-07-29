# -*- coding: utf-8 -*-

"""
@Project : lqbox 
@File    : __init__.py
@Date    : 2023/8/25 10:58:45
@Author  : zhchen
@Desc    : 
"""
import base64
import hashlib

import requests


class BaseBox:
    base_url = None

    def __init__(self, cookies):
        self.cookies = cookies
        self.check()

    def check(self):
        if not self.base_url:
            raise ValueError("base_url is None")

        self.base_url = self.base64(self.base_url)

    def request(self, method, url, **kwargs):
        if kwargs.get('headers') is None:
            kwargs['headers'] = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            }
        if kwargs.get("cookies") is None:
            kwargs['cookies'] = self.cookies
        return requests.request(method, url, **kwargs)

    @staticmethod
    def md5(string: str) -> str:
        """生成MD5"""
        hl = hashlib.md5()
        hl.update(string.encode(encoding='utf-8'))
        return hl.hexdigest()

    @staticmethod
    def base64(string: str) -> str:
        """base64解码"""
        decoded_bytes = base64.b64decode(string)
        return decoded_bytes.decode('utf-8')
