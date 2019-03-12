import json

import pytest
import requests


def test1(login_admin_headers):
    urls = "http://112.13.89.101:9011/v1/pc/common/currentConference/list/"
    if not login_admin_headers:
        pytest.xfail('登录失败')
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
