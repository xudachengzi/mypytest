import pytest


@pytest.mark.webtest
def test_send_http():
    pass


def test_something_quick():
    pass


def test_another():
    pass


class TestCase:
    def test_method(self):
        pass


if __name__ == '__main__':
    # pytest.main(['-s', 'test_server.py', "-m=webtest"])
    pytest.main(['-v', 'test_server.py'])
