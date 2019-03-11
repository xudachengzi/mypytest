import json

import pytest
import requests

host_data = 'http://112.13.89.101:9011'


user_data = [
    {
        "account": "admin",
        "mobile_phone": "",
        "password": "123456",
        "code": "",
        "way": "1",
        "source": "1"
    },
    {
        "account": "yzdbt",
        "mobile_phone": "",
        "password": "nbrd@123",
        "code": "",
        "way": "1",
        "source": "1"
    }
]


@pytest.fixture()
def login_admin_headers():
    url = host_data + '/v1/auth/login/'
    r = requests.post(url, data=user_data[0])
    di = json.loads(r.text)
    token = di['data']['user_info']['token']
    headers = {
        "Authorization": token
    }
    return headers


@pytest.fixture()
def login_worker_headers():
    url = host_data + '/v1/auth/login/'
    r = requests.post(url, data=user_data[1])
    di = json.loads(r.text)
    token = di['data']['user_info']['token']
    headers = {
        "Authorization": token
    }
    return headers
