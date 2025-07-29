# -*- coding: utf-8 -*-

"""
@Project : lqbox 
@File    : __init__.py
@Date    : 2024/2/2 17:19:22
@Author  : zhchen
@Desc    : 
"""
from lqbox.base import BaseBox


class McBox(BaseBox):
    base_url = 'aHR0cHM6Ly9tYy5sZXFlZS5jb20='

    def __init__(self, cookies):
        self.token = None
        super().__init__(cookies)

    def check(self):
        super().check()
        self.token = self.cookies.get("token")
        if not self.token:
            raise ValueError("token is None")

    def __mc_request(self, path, json_data):
        return self.request(url=f"{self.base_url}{path}", method="POST", json=json_data)

    def get_current_user_info(self):
        """获取用户信息"""
        return self.__mc_request(path='/api/UserController/getCurrentUserInfo', json_data={"token": self.token})

    def get_account_project(self, account: str):
        """获取日志project"""
        return self.__mc_request(
            path='/spore/api/sls/getAccountProject',
            json_data={'account': account, 'token': self.token}
        )

    def get_project_log_store(self, json_data):
        """获取对应的日志store"""
        # json_data = {
        #     'account': '123',
        #     'project': '123',
        # }
        return self.__mc_request(
            path='/spore/api/sls/getProjectLogStore',
            json_data={**json_data, "token": self.token}
        )

    def get_sls_iframe_url(self, json_data):
        """获取阿里云令牌url"""
        # json_data = {
        #     'account': '123',
        #     'project': '123',
        #     'logstore': '123',
        # }
        return self.__mc_request(
            path='/spore/api/sls/getSLSIframeUrl',
            json_data={**json_data, "token": self.token}
        )
