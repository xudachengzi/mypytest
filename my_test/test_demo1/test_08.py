import time
import pytest


@pytest.fixture(scope="module", autouse=True)  # start设置scope为module级别，在当前.py文件只执行一次，autouse=True自动使用
def start(request):
    print('\n-----开始执行module----')
    print('module      : %s' % request.module.__name__)
    print('----------启动浏览器---------')
    yield
    print("------------结束测试 end!-----------")


@pytest.fixture(scope="function", autouse=True)  # open_home设置scope为function级别，在每个用例前都调用一次
def open_home(request):
    print("function：%s \n--------回到首页--------" % request.function.__name__)


class TestCase:
    def test_01(self):
        print(3333)

    def test_02(self):
        print('4444')


if __name__ == '__main__':
    pytest.main(['-s', 'test_08.py'])
