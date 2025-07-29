# -*- coding: utf-8 -*-

"""
@Project : lqbox 
@File    : __init__.py
@Date    : 2023/8/25 10:51:23
@Author  : zhchen
@Desc    : 
"""
from lqbox.base import BaseBox


class ElihuBox(BaseBox):
    base_url = 'aHR0cHM6Ly9lbGlodS1taW5lci5sZXFlZS5jb20='

    def __elihu_request(self, path, json_data):
        return self.request(url=f"{self.base_url}{path}", method="POST", json=json_data)

    def _get_target_machine_list(self):
        """获取所有机器"""
        return self.__elihu_request(path="/api/ScheduleController/getTargetMachineList", json_data={})

    def queue_search(self, json_data):
        """查询队列"""
        # json_data = {
        #     'page': 1,
        #     'page_size': 10,
        #     'status': ['INIT', 'ENQUEUED', 'RUNNING', 'DONE', 'ERROR', 'DEAD', 'CANCELLED'],
        #     'task_id': '1234',
        #     'enqueue_time': [
        #         '2023/04/24 05:00:00',
        #         '2023/04/26 00:00:00',
        #     ],
        #     'title': 'API',
        #     'schedule_id': '1',
        #     'target_machine': 'machine002',
        # }
        return self.__elihu_request(path='/api/QueueController/listTasksInQueue', json_data=json_data)

    def queue_fork(self, json_data):
        """fork一个task"""
        # json_data = {
        #     'task_id': 1234,
        #     'enqueue_now': 'NO',
        # }
        return self.__elihu_request(path='/api/QueueController/forkTask', json_data=json_data)

    def queue_cancel(self, json_data):
        """取消一个任务到队列, task状态必须是INIT"""
        # json_data = {
        #     'task_id': 1234,
        # }
        return self.__elihu_request(path='/api/QueueController/cancelTask', json_data=json_data)

    def queue_enqueue(self, json_data):
        """进入队列"""
        # json_data = {
        #     'task_id': 1234,
        # }
        return self.__elihu_request(path='/api/QueueController/enqueueTask', json_data=json_data)

    def queue_mark_dead(self, json_data):
        """kill一个task, 并且会标记为ERROR"""
        # json_data = {
        #     'task_id': 1234,
        # }
        return self.__elihu_request(path='/api/QueueController/registerTimeoutForTask', json_data=json_data)

    def schedules_load(self, json_data):
        """查询调度时间"""
        # json_data = {
        #     'page': 1,
        #     'page_size': 10,
        #     'status': ['ON', 'OFF', 'NEVER'],
        #     'title': '123',
        #     'targetMachines': ['172.',],
        #     'commandSearchText': '123',
        # }
        return self.__elihu_request(path='/api/ScheduleController/fetchScheduleList', json_data=json_data)

    def schedules_run_once(self, json_data):
        """立即执行一次"""
        # json_data = {
        #     'schedule_id': 123,
        #     'enqueue_now': 'YES',
        # }
        return self.__elihu_request(path='/api/QueueController/createRunOnceTaskFromSchedule', json_data=json_data)

    def schedules_machine(self):
        """查询所有机器"""
        return self.__elihu_request(path='/api/ScheduleController/getTargetMachineList', json_data={})

    def cron_plan_fetch(self, json_data):
        """获取所有计划时间"""
        # json_data = {
        #     'start': '2024-01-01',
        #     'end': '2024-01-02',
        #     'target_machine_options': [],
        # }
        return self.__elihu_request(path='/api/StatController/fetchCronPlan', json_data=json_data)

    def schedules_edit(self, json_data):
        """编辑调度"""
        # json_data = {
        #     'schedule': {
        #         'task_id': 1,
        #         'task_title': '2',
        #         'task_type': '3',
        #         'cron_expression': '4',
        #         'command': '5',
        #         'task_status': 'ON',
        #         'priority': 10,
        #         'timeout': '0',
        #         'target_machine': '6',
        #         'request_user': '7',
        #         'current_request_user': '8',
        #         'locks': [],
        #         'shovel_project': '9',
        #         'shovel_class': '10',
        #     },
        # }
        return self.__elihu_request(path='/api/ScheduleController/editSchedule', json_data=json_data)

    def commands_new(self, json_data):
        """新建命令"""
        # json_data = {
        #     'target_machine': '',
        #     'param': {
        #         'script_name': '',
        #         'parameters': [''],
        #         'become': '',
        #     },
        #     'become': '',
        # }
        return self.__elihu_request(path='/api/CommandController/applyScriptCommand', json_data=json_data)

    def commands_list(self, json_data):
        """查询命令"""
        # json_data = {
        #     'page': 1,
        #     'page_size': 10,
        # }
        return self.__elihu_request(path='/api/CommandController/listCommands', json_data=json_data)
