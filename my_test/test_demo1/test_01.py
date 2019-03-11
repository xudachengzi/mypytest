# import pytest
# test_login_data = [
#     {'admin', '123456'},
#     {'admin', ''}
# ]
#
#
# def login(user, psw):
#     '''登录函数'''
#     print('登录账户：%s' % user)
#     print('登录密码：%s' % psw)
#     if psw:
#         return True
#     else:
#         return False
#
#
# @pytest.mark.parametrize('user,psw', test_login_data)
# def test_login(user, psw):
#     '''登录用例'''
#     result = login(user, psw)
#     assert result == True, '失败原因：密码错误'
#
#
# if __name__ == '__main__':
#     pytest.main(['-s', 'test_01.py'])
import json

import pytest
import requests


def test1(login_admin_headers):
    urls = "http://112.13.89.101:9011/v1/pc/common/currentConference/list/"
    r = requests.get(urls, headers=login_admin_headers)
    di = json.loads(r.text)
    assert di.get("code") == 0


def test2(login_worker_headers):
    urls = "http://112.13.89.101:9011/v1/pc/common/currentConference/list/"
    r = requests.get(urls, headers=login_worker_headers)
    di = json.loads(r.text)
    assert di.get("code") == 0


if __name__ == '__main__':
    pytest.main(['-s', 'test_01.py'])
