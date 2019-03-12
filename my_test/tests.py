import random
import unittest
import requests
import json
import HTMLTestRunner
import time
import pytest

import os

url = "http://112.13.89.101:9011"

# token admin的token
# a_token 工作人员余姚代表团的token
# all_delegation    所有代表团的列表
# delegation        余姚代表团的id
# conference        人代会的id
# delegation_topic_uuid 代表团议题的id
# delegation_worker_uuid 代表团工作人员的uuid
# rddb_id  示例人大代表id
# sms_id   短信uuid
# system_message_id  推送消息uuid
# delegation_group_id 代表团小组id


"""login 登录模块"""


class LoginTest(unittest.TestCase):
    """用户登录"""

    def setUp(self):
        self.url = url + "/v1/auth/login/"

    @pytest.mark.admin
    @pytest.mark.worker
    def test_case1(self):
        """超级管理员登录成功"""
        form = {
            "account": "admin",
            "mobile_phone": "",
            "password": "123456",
            "code": "",
            "way": "1",
            "source": "1"
        }
        r = requests.post(self.url, data=form)
        di = json.loads(r.text)
        global token
        token = di['data']['user_info']['token']
        # print(token)
        assert di.get('code') == 0

    @pytest.mark.worker
    @pytest.mark.admin
    def test_case2(self):
        """工作人员登录成功"""
        form = {
            "account": "yydbt",
            "mobile_phone": "",
            "password": "nbrd@123",
            "code": "",
            "way": "1",
            "source": "1"
        }
        r = requests.post(self.url, data=form)
        di = json.loads(r.text)
        global a_token
        a_token = di['data']['user_info']['token']
        print(a_token)
        assert di.get('code') == 0

    @pytest.mark.worker
    @pytest.mark.admin
    def test_case3(self):
        """人大代表登录成功"""
        form = {
            "account": "",
            "mobile_phone": "18815276687",
            "password": "",
            "code": "1234",
            "way": "3",
            "source": "2"
        }
        r = requests.post(self.url, data=form)
        di = json.loads(r.text)
        global r_token
        r_token = di['data']['user_info']['token']
        assert di.get('code') == 0

    def test_case6(self):
        """账号正确密码为空"""
        form = {
            "account": "admin",
            "mobile_phone": "",
            "password": "",
            "code": "",
            "way": "1",
            "source": "1"
        }
        r = requests.post(self.url, data=form)
        di = json.loads(r.text)

        assert di.get('code') == 1

    def test_case4(self):
        """账号正确密码错误"""
        form = {
            "account": "admin",
            "mobile_phone": "",
            "password": "111111",
            "code": "",
            "way": "1",
            "source": "1"
        }
        r = requests.post(self.url, data=form)
        di = json.loads(r.text)
        assert di.get('code') == 1

    def test_case5(self):
        """账号为空密码正确"""
        form = {
            "account": "",
            "mobile_phone": "",
            "password": "123456",
            "code": "",
            "way": "1",
            "source": "1"
        }
        r = requests.post(self.url, data=form)
        di = json.loads(r.text)
        assert di.get('code') == 1


class DelegationTest(unittest.TestCase):
    """获取所有代表团"""

    @pytest.mark.admin
    @pytest.mark.worker
    def test_case(self):
        """获取示例人大代表"""
        urls = url + "/v1/pc/common/logicGroup/list/?type=1,2,3,4"
        headers = {
            "Authorization": token
        }
        r = requests.get(urls, headers=headers)
        di = json.loads(r.text)
        global rddb_id
        rddb_id = di["data"][0]["users"][0]["id"]
        assert di.get("code") == 0

    @pytest.mark.admin
    @pytest.mark.worker
    def test_case1(self):
        """获取所有代表团"""
        urls = url + "/v1/pc/common/delegation/list/"
        headers = {
            "Authorization": token
        }
        r = requests.get(urls, headers=headers)
        di = json.loads(r.text)
        global all_delegation
        global delegation
        delegation = di["data"]["list"][0]["id"]
        print(delegation)
        all_delegation = di["data"]["list"]
        assert di.get("code") == 0

    @pytest.mark.admin
    def test_case2(self):
        """创建代表团成功"""
        urls = url + "/v1/pc/conference/delegation/add/"
        headers = {
            "Authorization": token
        }
        data = {
            'id': '',
            'team_count': '12',
            'name': '第八代表团',
            'remark': ''
        }

        r = requests.post(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0

    @pytest.mark.admin
    def test_case3(self):
        """获取所有代表团（包括小组）"""
        urls = url + "/v1/pc/common/delegation/list/"
        headers = {
            "Authorization": token
        }
        r = requests.get(urls, headers=headers)
        di = json.loads(r.text)
        global delegation_id
        for delegation in di['data']['list']:
            if delegation['name'] == '第八代表团':
                delegation_id = delegation['id']
        assert di.get("code") == 0

    @pytest.mark.admin
    def test_case4(self):
        """更新代表团成功"""
        urls = url + "/v1/pc/conference/delegation/update/" + delegation_id + "/"
        headers = {
            "Authorization": token
        }
        data = {
            'id': '',
            'team_count': '12',
            'name': '第九代表团',
            'remark': ''
        }
        r = requests.put(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0

    @pytest.mark.admin
    def test_case5(self):
        """删除代表团成功"""
        urls = url + "/v1/pc/conference/delegation/delete/"
        headers = {
            "Authorization": token
        }
        data = {
            'ids': delegation_id,
        }
        r = requests.post(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0


"""PC/conference 会议模块"""


class CurrentConferenceList(unittest.TestCase):
    """获取所有人代会"""

    @pytest.mark.admin
    @pytest.mark.worker
    def test_case(self):
        """获取所有人代会"""
        urls = url + "/v1/pc/common/currentConference/list/"
        headers = {
            "Authorization": token
        }
        r = requests.get(urls, headers=headers)
        di = json.loads(r.text)
        global conference
        conference = di["data"]["id"]
        assert di.get("code") == 0


class DelegationTopicTest(unittest.TestCase):
    """代表团议题相关"""

    @pytest.mark.worker
    def test_case1(self):
        """创建代表团议题——成功"""
        urls = url + "/v1/pc/conference/topic/add/"
        headers = {
            "Authorization": a_token
        }
        data = {
            "conference": conference,
            "delegation": delegation,
            "theme": "unittest测试",
            "content": "测试中"
        }
        r = requests.post(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0

    def test_case2(self):
        """创建代表团议题——内容为空请求失败"""
        urls = url + "/v1/pc/conference/topic/add/"
        headers = {
            "Authorization": token
        }
        data = {
            "conference": conference,
            "delegation": delegation,
            "theme": "unittest测试",
            "content": ""
        }
        r = requests.post(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 1

    @pytest.mark.admin
    @pytest.mark.worker
    def test_case3(self):
        """代表团议题查看"""
        urls = url + "/v1/pc/conference/topic/list/"
        headers = {
            "Authorization": token
        }

        r = requests.get(urls, headers=headers)
        di = json.loads(r.text)
        global delegation_topic_uuid
        delegation_topic_uuid = di["data"]['list'][0]["id"]
        assert di.get("code") == 0

    @pytest.mark.admin
    @pytest.mark.worker
    def test_case4(self):
        """代表团议题详情查看"""
        urls = url + "/v1/pc/conference/topic/get/" + delegation_topic_uuid + "/"
        headers = {
            "Authorization": token
        }
        r = requests.get(urls, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0

    @pytest.mark.admin
    @pytest.mark.worker
    def test_case5(self):
        """代表团议题——数据正确修改成功"""

        urls = url + "/v1/pc/conference/topic/update/" + delegation_topic_uuid + "/"
        headers = {
            "Authorization": token
        }
        data = {
            "conference": conference,
            "delegation": delegation,
            "theme": "修改pytest修改",
            "content": "完成修改"
        }
        r = requests.put(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0

    def test_case6(self):
        """代表团议题——content为空"""
        urls = url + "/v1/pc/conference/topic/update/" + delegation_topic_uuid + "/"
        headers = {
            "Authorization": token
        }
        data = {
            "conference": conference,
            "delegation": delegation,
            "theme": "修改为unittest修改",
            "content": ""
        }
        r = requests.put(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 1

    @pytest.mark.admin
    @pytest.mark.worker
    def test_case7(self):
        """代表团议题删除"""
        urls = url + "/v1/pc/conference/topic/delete/"
        headers = {
            "Authorization": token
        }
        data = {
            "ids": delegation_topic_uuid
        }
        r = requests.post(urls, data=data, headers=headers)
        di = json.loads(r.text)
        print(di)
        assert di.get("code") == 0


class DelegationPubTest(unittest.TestCase):
    """代表团公告相关"""

    @pytest.mark.admin
    def test_case1(self):
        """添加公告成功"""
        urls = url + "/v1/pc/conference/topic/savePub/"
        headers = {
            "Authorization": token
        }
        data = {
            "end_time": "2018-12-25T13:25",
            "content": "议题新增测试"
        }
        r = requests.post(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0

    def test_case2(self):
        """添加公告失败——content为空"""
        urls = url + "/v1/pc/conference/topic/savePub/"
        headers = {
            "Authorization": token
        }
        data = {
            "end_time": "2018-12-25T13:25",
            "content": ""
        }
        r = requests.post(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 1

    @pytest.mark.worker
    def test_case3(self):
        """获取公告成功"""
        urls = url + "/v1/pc/conference/topic/getPub/"
        headers = {
            "Authorization": a_token
        }

        r = requests.get(urls, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0

    @pytest.mark.admin
    def test_case4(self):
        """添加工作人员公告"""
        urls = url + "/v1/pc/conference/delegationWorker/savePub/"
        headers = {
            "Authorization": a_token
        }
        data = {
            "end_time": "2018-12-25T13:25",
            "content": "工作人员公告新增"
        }
        r = requests.post(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0

    @pytest.mark.worker
    def test_case5(self):
        """查看工作人员公告"""
        urls = url + "/v1/pc/conference/delegationWorker/getPub/"
        headers = {
            "Authorization": a_token
        }

        r = requests.get(urls, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0


class DelegationCardNumTest(unittest.TestCase):
    """代表团卡数量相关"""

    @pytest.mark.admin
    def test_case1(self):
        """添加代表团卡数成功"""
        urls = url + "/v1/pc/conference/delegationWorker/setCardNum/" + delegation + "/"
        headers = {
            "Authorization": token
        }
        data = {
            "a_card": "30",
            "b_card": "2",
            "blank": "1"
        }
        r = requests.put(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0

    def test_case2(self):
        """添加代表团卡数失败"""
        urls = url + "/v1/pc/conference/delegationWorker/setCardNum/" + delegation + "/"
        headers = {
            "Authorization": token
        }
        data = {
            "a_card": "a",
            "b_card": "-1",
            "blank": "1"
        }
        r = requests.put(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 1

    @pytest.mark.admin
    @pytest.mark.worker
    def test_case3(self):
        """获取单个代表团卡数成功"""
        urls = url + "/v1/pc/conference/delegationWorker/getCardNum/" + delegation + "/"
        headers = {
            "Authorization": a_token
        }

        r = requests.get(urls, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0


class DelegationWorkerTest(unittest.TestCase):
    """代表团工作人员相关"""

    @pytest.mark.worker
    def test_case1(self):
        """增加代表团工作人员成功"""
        urls = url + "/v1/pc/conference/delegationWorker/add/"
        mobile_phone = "156" + str(random.randint(10000000, 99999999))
        data = {
            "group_type": '1',
            "username": "测试人",
            "mobile_phone": mobile_phone,
            "card_type": "1",
            "delegation": delegation,
            "picture": "test.png"
        }
        headers = {
            "Authorization": a_token
        }
        r = requests.post(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0

    def test_case2(self):
        """增加代表团工作人员失败——内容不完整picture为空"""
        urls = url + "/v1/pc/conference/delegationWorker/add/"
        data = {
            "group_type": '1',
            "username": "测试人",
            "mobile_phone": "15515140077",
            "card_type": "1",
            "delegation": delegation,
            "picture": ""
        }
        headers = {
            "Authorization": a_token
        }
        r = requests.post(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 1

    def test_case3(self):
        """增加代表团工作人员失败——增加失败手机号含有字符"""
        urls = url + "/v1/pc/conference/delegationWorker/add/"
        data = {
            "group_type": '1',
            "username": "测试人",
            "mobile_phone": "1551514007p",
            "card_type": "1",
            "delegation": delegation,
            "picture": ""
        }
        headers = {
            "Authorization": a_token
        }
        r = requests.post(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 1

    @pytest.mark.worker
    @pytest.mark.admin
    def test_case4(self):
        """查看代表团工作人员"""
        urls = url + "/v1/pc/conference/delegationWorker/list/"
        headers = {
            "Authorization": a_token
        }
        r = requests.get(urls, headers=headers)
        di = json.loads(r.text)
        global delegation_worker_uuid
        delegation_worker_uuid = di["data"]["list"][0]["id"]
        assert di.get("code") == 0

    @pytest.mark.admin
    def test_case5(self):
        """以卡数量获取所有代表团工作人员成功"""
        urls = url + "/v1/pc/conference/delegationWorker/cardlist/"
        headers = {
            "Authorization": a_token
        }
        params = {
            "delagation": delegation
        }

        r = requests.get(url=urls, params=params, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0

    @pytest.mark.admin
    @pytest.mark.worker
    def test_case6(self):
        """查看代表团工作人员详情"""
        urls = url + "/v1/pc/conference/delegationWorker/get/" + delegation_worker_uuid + "/"
        headers = {
            "Authorization": a_token
        }

        r = requests.get(urls, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0

    @pytest.mark.admin
    @pytest.mark.worker
    def test_case7(self):
        """设置快捷联系人成功"""
        urls = url + "/v1/pc/conference/delegationWorker/setQuickContact/"
        headers = {
            "Authorization": a_token
        }
        data = {
            "ids": delegation_worker_uuid

        }
        r = requests.post(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0

    @pytest.mark.admin
    @pytest.mark.worker
    def test_case8(self):
        """更新代表团人员"""
        urls = url + "/v1/pc/conference/delegationWorker/update/" + delegation_worker_uuid + "/"
        mobile_phone = "156" + str(random.randint(10000000, 99999999))
        headers = {
            "Authorization": a_token
        }
        print(delegation_worker_uuid)
        data = {
            "group_type": '1',
            "username": "测试人",
            "mobile_phone": mobile_phone,
            "card_type": "1",
            "delegation": delegation,
            "picture": "test.png"
        }
        r = requests.put(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0

    @pytest.mark.admin
    @pytest.mark.worker
    def test_case9(self):
        """删除成功"""
        urls = url + "/v1/pc/conference/delegationWorker/delete/"
        headers = {
            "Authorization": a_token
        }
        data = {
            "ids": delegation_worker_uuid
        }
        r = requests.post(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0


class AddUserTest(unittest.TestCase):
    @pytest.mark.worker
    @pytest.mark.skip(reason='不知道传参')
    def test_case1(self):
        """代表团人员绑定"""
        urls = url + "/v1/pc/conference/delegation/add_user/ "
        data = {
            "ids": rddb_id,
        }
        headers = {
            "Authorization": a_token
        }
        r = requests.post(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0


class DelegationGroupTest(unittest.TestCase):
    """代表团小组相关"""

    @pytest.mark.admin
    def test_case1(self):
        """创建代表团小组"""
        urls = url + "/v1/pc/conference/delegationGroup/create/"
        data = {
            'id': '',
            'name': '测试小组',
            'delegation': delegation,
            'meeting_venue': ''
        }
        headers = {
            "Authorization": token
        }
        r = requests.post(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0

    @pytest.mark.admin
    def test_case2(self):
        """获取代表团小组"""
        urls = url + "/v1/pc/conference/delegationGroups/list/"

        headers = {
            "Authorization": token
        }
        global delegation_group_id
        r = requests.get(urls, headers=headers)
        di = json.loads(r.text)
        delegation_group_id = di['data']['list'][0]['id']
        assert di.get("code") == 0


"""PC/communication 消息模块"""


class SmsSendTest(unittest.TestCase):
    """短信相关"""

    @pytest.mark.admin
    @pytest.mark.worker
    def test_case1(self):
        """创建短信成功"""
        urls = url + "/v1/pc/communication/smsSend/create/"
        headers = {
            "Authorization": a_token
        }
        data = {
            "ids": rddb_id,
            "content": "发送短信测试",
            "type": '1',
            "send_date": ''
        }
        r = requests.post(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0

    def test_case2(self):
        """创建短信失败——content为空请求成功"""
        urls = url + "/v1/pc/communication/smsSend/create/"
        headers = {
            "Authorization": a_token
        }
        data = {
            "ids": rddb_id,
            "content": "",
            "type": '1',
            "send_date": ''
        }
        r = requests.post(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 1

    def test_case3(self):
        """创建短信失败——type为空请求失败"""
        urls = url + "/v1/pc/communication/smsSend/create/"
        headers = {
            "Authorization": a_token
        }
        data = {
            "ids": rddb_id,
            "content": "测试",
            "type": '',
            "send_date": ''
        }
        r = requests.post(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 1

    @pytest.mark.admin
    @pytest.mark.worker
    def test_case4(self):
        """查看短信消息列表"""
        urls = url + "/v1/pc/communication/smsSend/list/"
        headers = {
            "Authorization": a_token
        }

        r = requests.get(urls, headers=headers)
        di = json.loads(r.text)
        global sms_id
        sms_id = di['data']['list'][0]["id"]
        assert di.get("code") == 0

    @pytest.mark.admin
    @pytest.mark.worker
    def test_case5(self):
        """查看短信消息详情"""
        urls = url + "/v1/pc/communication/smsSend/get/" + sms_id + "/"
        headers = {
            "Authorization": a_token
        }
        r = requests.get(urls, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0

    @pytest.mark.worker
    @pytest.mark.admin
    def test_case6(self):
        """删除未发送的短信"""
        urls = url + "/v1/pc/communication/smsSend/delete/"
        headers = {
            "Authorization": token
        }
        data = {
            'ids': sms_id,
        }
        r = requests.post(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0

    @pytest.mark.admin
    def test_case7(self):
        """创建智能短信"""
        urls = url + "/v1/pc/communication/smartSms/create/"
        headers = {
            "Authorization": token
        }
        data = {
            'ids': rddb_id,
            'content': '1',
            'type': 1,
            'smart_type': 1,
            'send_date': '2018-12-15 15:15:15'
        }
        r = requests.post(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0


class SmsDelegationConfigTest(unittest.TestCase):
    """代表团下发送短信数量和设置的上限"""

    @pytest.mark.admin
    def test_case1(self):
        """代表团下列席人员查询成功"""
        urls = url + "/v1/pc/communication/smsDelegationConfig/list/"
        headers = {
            "Authorization": a_token
        }

        r = requests.get(urls, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0

    @pytest.mark.admin
    def test_case2(self):
        """更新各个代表团短信配置"""
        urls = url + "/v1/pc/communication/smsDelegationConfig/update/"
        headers = {
            "Authorization": a_token,
            "Content-Type": "application/json"
        }
        data = json.dumps(
            [{"id": "37f3d8e4-08fa-11e9-9939-e0d55e8f2d9a", "max_sms_num": 1000, "delegation_name": "余姚代表团"},
             {"id": "37f5aa62-08fa-11e9-90af-e0d55e8f2d9a", "max_sms_num": 1000, "delegation_name": "慈溪代表团"},
             {"id": "37f7588c-08fa-11e9-827e-e0d55e8f2d9a", "max_sms_num": 1000, "delegation_name": "鄞州代表团"},
             {"id": "37f9093e-08fa-11e9-801c-e0d55e8f2d9a", "max_sms_num": 1000, "delegation_name": "海曙代表团"},
             {"id": "37fab878-08fa-11e9-8722-e0d55e8f2d9a", "max_sms_num": 1000, "delegation_name": "北仑代表团"},
             {"id": "37fc43ec-08fa-11e9-8618-e0d55e8f2d9a", "max_sms_num": 1000, "delegation_name": "江北代表团"},
             {"id": "37fe1946-08fa-11e9-8294-e0d55e8f2d9a", "max_sms_num": 1000, "delegation_name": "镇海代表团"},
             {"id": "380014fe-08fa-11e9-b32e-e0d55e8f2d9a", "max_sms_num": 1000, "delegation_name": "奉化代表团"},
             {"id": "38025f46-08fa-11e9-bdd1-e0d55e8f2d9a", "max_sms_num": 1000, "delegation_name": "象山代表团"},
             {"id": "380483c6-08fa-11e9-b03f-e0d55e8f2d9a", "max_sms_num": 1000, "delegation_name": "宁海代表团"},
             {"id": "3806cb40-08fa-11e9-a96c-e0d55e8f2d9a", "max_sms_num": 1000, "delegation_name": "驻甬部队代表团"}])

        r = requests.post(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0


class ChatRoomTest(unittest.TestCase):
    """聊天房间相关（暂无）"""

    @pytest.mark.skip(reason='接口未调通')
    def test_case1(self):  # 暂无
        """获取小组列表"""
        urls = url + '/v1/pc/communication/chatRoom/list/'
        pass

    @pytest.mark.skip(reason='接口未调通')
    def test_case2(self):  # 暂无
        """创建聊天房间"""
        urls = url + '/v1/pc/communication/chatRoom/create/'
        pass

    @pytest.mark.skip(reason='接口未调通')
    def test_case3(self):  # 暂无
        """更新聊天房间"""
        urls = url + '/v1/pc/communication/chatRoom/update/<id>/'
        pass

    @pytest.mark.skip(reason='接口未调通')
    def test_case4(self):  # 暂无
        """聊天房间——消息记录"""
        urls = url + '/v1/pc/communication/chatRoom/msgList/'
        pass

    @pytest.mark.skip(reason='接口未调通')
    def test_case5(self):  # 暂无
        """删除聊天房间"""
        urls = url + '/v1/pc/communication/chatRoom/delete/'
        pass


class SystemMessageTest(unittest.TestCase):
    """系统消息相关"""

    @pytest.mark.admin
    def test_case1(self):
        """创建系统消息成功"""
        urls = url + "/v1/pc/communication/sysMsgPush/createSysMsg/"
        headers = {
            "Authorization": a_token
        }
        data = {
            'content': '123',
            'title': '123',
        }

        r = requests.post(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0

    def test_case2(self):
        """创建系统消息失败——不填写内容"""
        urls = url + "/v1/pc/communication/sysMsgPush/createSysMsg/"
        headers = {
            "Authorization": a_token
        }
        data = {
            'content': '',
            'title': '',
        }

        r = requests.post(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 1

    @pytest.mark.skip(reason='涉及图片上传')
    def test_case3(self):
        """创建每日推送成功"""
        urls = url + "/v1/pc/communication/sysMsgPush/createDayPush/"
        headers = {
            "Authorization": a_token
        }
        data = {
            'content': '123',
            'title': '123',
            'link_url': '',
            'main_img': '1',  # 涉及图片上传
            'summary': '12'
        }

        r = requests.post(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0

    @pytest.mark.admin
    def test_case4(self):
        """查看推送系统列表"""
        urls = url + "/v1/pc/communication/sysMsgPush/getSystemPushMsgList/"
        headers = {
            "Authorization": token
        }
        global system_message_id
        r = requests.get(urls, headers=headers)
        di = json.loads(r.text)
        system_message_id = di['data']['list'][0]['id']
        assert di.get("code") == 0

    @pytest.mark.admin
    @pytest.mark.skip()
    def test_case5(self):
        """修改系统消息发布状态"""
        urls = url + "/v1/pc/communication/sysMsgPush/updatePubStatus/"
        headers = {
            "Authorization": token
        }
        data = {
            'id': system_message_id,
            'is_pub': 1,
        }
        r = requests.post(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0

    @pytest.mark.admin
    def test_case6(self):
        """创建系统公告消息成功"""
        urls = url + "/v1/pc/communication/sysMsgPush/createSysPub/"
        headers = {
            "Authorization": token
        }
        data = {
            'content': '123',
        }
        r = requests.post(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0

    def test_case7(self):
        """创建系统公告消息失败——不填写内容"""
        urls = url + "/v1/pc/communication/sysMsgPush/createSysPub/"
        headers = {
            "Authorization": token
        }
        data = {
            'content': '',
        }
        r = requests.post(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 1

    @pytest.mark.admin
    def test_case8(self):
        """获取系统公告消息成功"""
        urls = url + "/v1/pc/communication/sysMsgPush/getSysPubList/"
        headers = {
            "Authorization": token
        }
        r = requests.get(urls, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0

    @pytest.mark.admin
    @pytest.mark.skip(reason='接口有误')
    def test_case9(self):
        """创建预览消息 每日推送"""
        urls = url + "/v1/pc/communication/sysMsgPush/createPreview/"
        headers = {
            "Authorization": token
        }
        data = {
            'preview_user': rddb_id,
            'res_type': 1,
            'res_id': system_message_id
        }
        r = requests.post(urls, data=data, headers=headers)
        di = json.loads(r.text)
        assert di.get("code") == 0
