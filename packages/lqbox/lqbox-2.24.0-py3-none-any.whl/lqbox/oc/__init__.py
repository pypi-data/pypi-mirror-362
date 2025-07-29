# -*- coding: utf-8 -*-

"""
@Project : lqbox 
@File    : __init__.py
@Date    : 2023/8/25 10:51:57
@Author  : zhchen
@Desc    : 
"""
from lqbox.base import BaseBox


class OcBox(BaseBox):
    base_url = 'aHR0cHM6Ly9vYy5sZXFlZS5jb20='

    def __init__(self, cookies):
        self.token = None
        super().__init__(cookies)

    def check(self):
        super().check()
        self.token = self.cookies.get("token")
        if not self.token:
            raise ValueError("token is None")

    def __oc_request(self, path, json_data):
        return self.request(url=f"{self.base_url}{path}", method="POST", json=json_data)

    def user_info_detail(self):
        """个人信息"""
        return self.__oc_request(
            path="/index.php/tachiba/TachibaServiceBasicInfoController/userInfoDetail",
            json_data={"token": self.token}
        )

    def display_user(self, json_data):
        """用户信息-新版"""
        # json_data = {
        #     "core_user_id": 1234
        # }
        return self.__oc_request(
            path="/ext-hr/api/staffProfile/StaffController/displayUser",
            json_data={**json_data, "token": self.token}
        )

    def assessing_list(self, json_data):
        """绩效列表"""
        # json_data = {
        #     'page': 1,
        #     'limit': 10,
        # }
        return self.__oc_request(
            path="/ext-hr/api/assessment/AssessmentAsAssesseeController/getMySelfAssessingList",
            json_data={**json_data, "token": self.token}
        )

    def assessing_result(self, json_data):
        """绩效具体"""
        # json_data = {
        #     "assessment_code": "2021Q04"
        # }
        return self.__oc_request(
            path="/ext-hr/api/assessment/AssessmentAsAssesseeController/getMySelfAssessingResult",
            json_data={**json_data, "token": self.token}
        )

    def team_building_fee(self, json_data):
        """团建费用"""
        # json_data = {
        #     'page': 1,
        #     'page_size': 10,
        #     'core_user_id': '',
        #     'department_id': '187',
        #     'year': 2021,
        # }
        return self.__oc_request(
            path="/index.php/oa/OaTeambuildingIssueController/getTeambuildingFeeList",
            json_data={**json_data, "token": self.token}
        )
