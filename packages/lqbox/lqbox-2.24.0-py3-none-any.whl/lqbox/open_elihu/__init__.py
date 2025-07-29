# -*- coding: utf-8 -*-

"""
@Project : lqbox 
@File    : __init__.py.py
@Date    : 2023/8/28 11:00:58
@Author  : zhchen
@Desc    : 
"""
import datetime
from typing import List, Iterable, Optional

from requests import Response

from lqbox.base import BaseBox


class OpenElihuBox(BaseBox):
    base_url = "aHR0cHM6Ly9lbGlodS1taW5lci5sZXFlZS5jb20vb3BlbmFwaQ=="
    name1 = 'ZWxpaHUtb3Blbi1hcGktdHAtY29kZQ=='
    name2 = 'ZWxpaHUtb3Blbi1hcGktbm9pc2U='
    name3 = 'ZWxpaHUtb3Blbi1hcGktY2hlY2tzdW0='

    def __init__(self, tp_code, tp_secret):
        super().__init__(cookies={})
        self.tp_code = tp_code
        self.tp_secret = tp_secret

    def request_open_api(self, api_path, body) -> Response:
        now = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        body[self.base64(self.name1)] = self.tp_code
        body[self.base64(self.name2)] = now
        body[self.base64(self.name3)] = self.md5(f'{self.tp_code}{now}{self.tp_secret}')
        r = self.request(method='POST', url=f'{self.base_url}/{api_path}', json=body)
        return r

    def call_check_task_detail(self, task_id: int) -> Response:
        """获取某个任务的状态"""
        return self.request_open_api(
            api_path="QueueOpenApiController/checkTaskDetail",
            body={"task_id": task_id}
        )

    def call_get_shovel_request_related_accounts(
            self,
            shovel_request_code: str,
            platform_code=None,
            shop_list=None,
            account_id=None
    ) -> Response:
        """获取账号"""
        dictionary = {
            "shovel_request_code": shovel_request_code,
        }
        if platform_code is not None:
            dictionary['platform_code'] = platform_code
        if shop_list is not None:
            dictionary['shop_list'] = shop_list
        if account_id is not None:
            dictionary['account_id'] = account_id

        return self.request_open_api(
            "KaiwaOpenApiController/getShovelRequestRelatedAccounts",
            dictionary
        )

    def call_get_accounts_without_long_session(self, account_id_list: List[int], platform_code: str) -> Response:
        """筛选出没有可用的 LONG 类型的会话的 account_id"""
        return self.request_open_api(
            'KaiwaOpenApiController/getAccountsWithoutLongSession',
            {'account_id_list': account_id_list, 'platform_code': platform_code}
        )

    def call_get_count_of_special_cookie(self, name: str):
        """获取特殊cookie的数量"""
        return self.request_open_api('KaiwaOpenApiController/getCountOfSpecialCookie', {'name': name})

    def call_get_count_of_unused_valid_special_cookie(self, name: str):
        return self.request_open_api('KaiwaOpenApiController/getUnusedCountOfValidSpecialCookie',
                                     {'name': name})

    def call_request_one_time_shovel_task(
            self,
            task_title: str,
            target_machine: str,
            shovel_project: str,
            shovel_class: str,
            shovel_extra: dict = None,
            locks: Iterable[dict] = None
    ) -> Response:
        """
        发起一个单次Shovel任务
        :param task_title:
        :param target_machine:
        :param shovel_project:
        :param shovel_class:
        :param shovel_extra:
        :param locks: format: {lock_name: '', addition: ''}
        :return:
        """
        payload = {
            "task_title": task_title,
            "target_machine": target_machine,
            "shovel_project": shovel_project,
            "shovel_class": shovel_class,
        }
        if shovel_extra is not None:
            payload['shovel_extra'] = shovel_extra
        if locks is not None:
            payload['locks'] = locks
        return self.request_open_api(
            "QueueOpenApiController/requestOneTimeShovelTask",
            payload
        )

    def call_get_account_related_available_sessions(
            self, account_id: int, platform_code: str,
            status: Optional[str] = None, limit: Optional[int] = None
    ) -> Response:
        """
        查找某个账号是否有可用会话 (获取session)
        :param account_id:
        :param platform_code: Since 1.18.27
        :param status: 不传的话默认填写 LONG 类型
        :param limit: 不传的话默认1
        :return:
        """
        dictionary = {
            'accountId': account_id,
            'platformCode': platform_code,
        }
        if status is not None:
            dictionary['status'] = status
        if limit is not None:
            dictionary['limit'] = limit
        else:
            dictionary['limit'] = 1

        return self.request_open_api(
            "AccountOpenApi/getAccountRelatedAvailableSessions",
            dictionary
        )
