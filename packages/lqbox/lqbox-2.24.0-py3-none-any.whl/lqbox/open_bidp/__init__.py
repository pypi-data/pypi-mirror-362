# -*- coding: utf-8 -*-

"""
@Project : lqbox 
@File    : __init__.py
@Date    : 2023/8/31 13:01:27
@Author  : zhchen
@Desc    : 
"""
import uuid
from typing import Optional

from requests import Response

from lqbox.base import BaseBox


class OpenBidpBox(BaseBox):
    base_url = 'aHR0cHM6Ly9iaWRwLmxlcWVlLmNvbS9vcGVuLXNlcnZpY2U='
    name1 = 'YXBwS2V5'
    name2 = 'bm9uY2U='
    name3 = 'c2lnbg=='

    def __init__(self, app_key, app_secret):
        super().__init__(cookies={})
        self.app_key = app_key
        self.app_secret = app_secret

    def request_open_api(self, api_path, body) -> Response:
        headers = {'content-type': 'application/json'}
        _uuid = str(uuid.uuid4())
        body[self.base64(self.name1)] = self.app_key
        body[self.base64(self.name2)] = _uuid
        body[self.base64(self.name3)] = self.md5(f'{self.app_key}@{_uuid}@{self.app_secret}')
        r = self.request(method="POST", url=f'{self.base_url}/{api_path}', json=body, headers=headers)
        return r

    def call_get_login_acc(self, platform_code=None, shop_list=None, account_id=None, channel=None):
        """获取登录的账号"""
        dictionary = {"platformCodes": platform_code}
        if shop_list is not None:
            dictionary['shopIds'] = shop_list
        if account_id is not None:
            dictionary['accountIds'] = account_id
        if channel is not None:
            dictionary['channel'] = channel
        return self.request_open_api("AccountOpenApi/getLoginAcc", dictionary)

    def call_get_accounts_without_long_session(self, account_id_list, platform_code=None):
        """筛选出没有可用的 LONG 类型的会话的 account_id"""
        d = {'accountIdList': account_id_list}
        if platform_code is not None:
            d['platformCode'] = platform_code
        return self.request_open_api('AccountOpenApi/getAccountsWithoutLongSession', body=d)

    def call_search_data_fetch_records(self, request_entity: dict):
        """检查之前的数据落盘记录，在补录场景下可以减少重复取数"""
        # request_entity的key: shovelProject, shovelClass, limit, aspect, partKey, timeRange, mizarGroupId
        return self.request_open_api('RecordOpenApiController/searchDataFetchRecords', body=request_entity)

    def call_get_account_related_available_sessions(
            self, account_id: int, platform_code: str,
            status: Optional[str] = None, limit: Optional[int] = None):
        """查找某个账号是否有可用会话 (获取session)"""
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

        return self.request_open_api("AccountOpenApi/getAccountRelatedAvailableSessions", body=dictionary)
