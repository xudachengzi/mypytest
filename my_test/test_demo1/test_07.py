import time
import pytest


@pytest.fixture(scope="function")
def start():
    return 11111


@pytest.mark.usefixtures('start')
def test_a():
    print(start())


@pytest.mark.usefixtures('start')
class Test_aaa:
    def test_01(self):
        print(3333)

    def test_02(self):
        print('4444')


if __name__ == '__main__':
    pytest.main(['-s', 'test_07.py'])