import time
import pytest


@pytest.fixture(scope="function")
def start(request):
    return 11111


def test_a(start):
    print(start)


class Test_aaa:
    def test_01(self, start):
        print('3333')

    def test_02(self, start):
        print('4444')


if __name__ == '__main__':
    pytest.main(['-s', 'test_06.py'])
