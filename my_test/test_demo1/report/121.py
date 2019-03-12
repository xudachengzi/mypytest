import pytest

canshu = [{'user': 'admin', 'psw': '11'}]


@pytest.fixture(scope='module')
def login(request):
    user = request.param['user']
    psw = request.param['psw']
    print('正在登录账号：%s，密码：%s') % (user, psw)
    if psw:
        return True
    else:
        return False


@pytest.mark.parametrize('login', canshu, indirect=True)
class TestXX:

    def test_01(self):
        '''用例1登录'''
        result = login
        print('用例1：%s' % result)
        assert result == True

    def test_02(self):
        '''用例2登录'''
        result = login
        print('用例1：%s' % result)
        if not result:
            pytest.xfail('登录不成功,标记为xfail')
        assert 1 == 1

    def test_03(self):
        '''用例3登录'''
        result = login
        print('用例1：%s' % result)
        if not result:
            pytest.xfail('登录不成功,标记为xfail')
        assert 1 == 1


if __name__ == '__main__':
    pytest.main(['-s', '121.py'])