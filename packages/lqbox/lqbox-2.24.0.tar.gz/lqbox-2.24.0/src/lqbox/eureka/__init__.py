# -*- coding: utf-8 -*-

"""
@Project : lqbox 
@File    : __init__.py.py
@Date    : 2024/10/9 13:10:33
@Author  : luke
@Desc    : 
"""
import os

from lqbox.base import BaseBox


class EurekaBox(BaseBox):
    base_url = 'aHR0cHM6Ly9lZS5sZXFlZS5jb20='

    def __init__(self, cookies):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
        }
        super().__init__(cookies)

    def chat_file_upload(self, file_path, file_type='image/png'):
        """上传聊天文件"""
        files = {
            'file': (os.path.basename(file_path), open(file_path, 'rb'), file_type),
        }
        response = self.request(
            method='POST',
            url=f'{self.base_url}/ee/proxy/ai/web/eureka/chat/session/file/upload',
            cookies=self.cookies,
            headers=self.headers,
            files=files,
        )
        return response
