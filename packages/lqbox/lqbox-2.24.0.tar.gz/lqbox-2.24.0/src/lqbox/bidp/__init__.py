# -*- coding: utf-8 -*-

"""
@Project : lqbox 
@File    : __init__.py
@Date    : 2023/8/25 10:51:45
@Author  : zhchen
@Desc    : 
"""
from lqbox.base import BaseBox


class BidpBox(BaseBox):
    base_url = 'aHR0cHM6Ly9iaWRwLmxlcWVlLmNvbQ=='

    def __init__(self, cookies):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/122.0.0.0 Safari/537.36',
            'authorization': None
        }
        super().__init__(cookies)

    def check(self):
        super().check()
        if not self.cookies.get('token'):
            raise ValueError('cookies中需要包含token')
        self.headers['authorization'] = self.cookies['token']

    def request(self, method, url, **kwargs):
        if kwargs.get('headers') is None:
            kwargs['headers'] = self.headers
        return super().request(method, url, **kwargs)

    def bidp_request(self, path, data, json=False):
        if json:
            return self.request(url=f"{self.base_url}{path}", method="POST", json=data)
        else:
            return self.request(url=f"{self.base_url}{path}", method="POST", data=data)

    # --== 需求模块 ==--
    def demand_detail(self, base_id):
        """需求详情"""
        data = {'baseId': str(base_id)}
        return self.bidp_request(path='/bi/controller/wb/DataWbBase/getDetail', data=data)

    def demand_module(self, base_id):
        """需求详情-成本排期-多人模块"""
        data = {'baseId': str(base_id)}
        return self.bidp_request(path='/bi/controller/wb/module/DataWbModule/getModuleStaff', data=data)

    def demand_module_task(self, base_id, module_id):
        """需求详情-多人模块-具体"""
        data = {
            'baseId': str(base_id),
            'moduleId': str(module_id),
        }
        return self.bidp_request(path='/bi/controller/wb/task/DataWbTask/getModuleTask', data=data)

    def demand_note_list(self, base_id):
        """需求详情-留言列表"""
        data = {'baseId': str(base_id)}
        return self.bidp_request(path='/bi/controller/wb/DataWbNote/listNote', data=data)

    # ++-- 需求模块 --++

    # --== 质量管理中心 ==--
    def monitor_alert_category(self):
        """数据采集中心-异常信息-所有分类"""
        return self.bidp_request(
            path='/bi/controller/crawler/monitor/CrawlerMonitorTaskExecuteResult/getAlertCategory', data={})

    def monitor_alert_list(self, data):
        """数据采集中心-异常信息"""
        # data = {
        #     'alertId': '123',
        #     'category': 'Cookie Invalidated',
        #     'pageNum': '1',
        #     'pageSize': '10',
        #     'startTime': '2024-04-10 00:00:00',
        #     'endTime': '2024-04-12 00:00:00',
        # }
        return self.bidp_request(
            path='/bi/controller/crawler/monitor/CrawlerMonitorTaskExecuteResult/alertList', data=data)

    def etl_task_list(self, data):
        """数据任务监控-任务管理"""
        # json_data = {
        #     'tableName': '',
        #     'tableCode': '123',
        #     'jobId': '',
        #     'pageNum': 1,
        #     'pageSize': 300,
        # }
        return self.bidp_request(path='/bi/controller/task/define/list', data=data, json=True)

    def etl_db_task(self, data):
        """入库任务监控-入库任务"""
        # data = {
        #     'taskId': '123',
        #     'pageNum': '1',
        #     'pageSize': '30',
        # }
        return self.bidp_request('/bi/controller/monitor/sync/toDbTask/list', data=data)

    # ++-- 质量管理中心 --++

    # --== 模型设计中心 == --
    def get_path_list(self):
        """模型建设-规范建表-采集路径"""
        return self.bidp_request(path='/bi/controller/crawler/manage/CrawlerManageNodeInfo/getPathList', data={})

    # ++-- 模型设计中心  --++

    # //-- 数据治理中心  --\\
    def search_relation_tables(self, data):
        """血缘分析-搜索血缘"""
        # data = {
        #     'searchInfo': '123',
        # }
        return self.bidp_request(path='/bi/controller/assets/TableRelation/searchTables', data=data)

    def get_relation(self, data):
        """血缘分析-获取血缘关系图"""
        # data = {
        #     'tableName': '123',
        #     'tableType': '123',
        #     'id': '123',
        #     'relationType': '123',
        # }
        return self.bidp_request(path='/bi/controller/assets/TableRelation/getRelation', data=data)

    def relation_table_base_info(self, data):
        """血缘分析-血缘关系图-点击某个节点"""
        # data = {
        #     'tableType': '123',
        #     'id': '123',
        # }
        return self.bidp_request(path='/bi/controller/assets/TableRelation/getBaseInfo', data=data)

    def meta_eb_collection(self, data):
        """元数据管理-数据集元数据-搜索列表页"""
        # data = {
        #     "pageNum": "1",
        #     "pageSize": "123",
        #     "collectionId": "123",
        #     "owner": "123",
        #     "collectionLevel": "123",
        #     "updatePeriod": "123",
        # }
        return self.bidp_request(path='/bi/controller/assets/MetaEbCollection/list', data=data)

    # //-- 数据治理中心  --\\
