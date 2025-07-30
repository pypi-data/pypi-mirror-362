import time
from unittest.mock import Mock
from pydecora.decorators.cache import cache


def test_default_parameters():
    mock_func = Mock(return_value="ok")

    @cache()
    def wrapped(a, b):
        return mock_func()

    wrapped(1, 2)
    wrapped(1, 2)

    assert mock_func.call_count == 1


def test_max_size():
    mock_func = Mock(return_value="ok")

    @cache(max_size=1)
    def wrapped(a, b):
        return mock_func()

    wrapped(1, 2)
    wrapped(1, 2)

    assert mock_func.call_count == 1

    wrapped(2, 3)
    wrapped(1, 2)

    assert mock_func.call_count == 3


def test_ttl():
    mock_func = Mock(return_value="ok")

    @cache(ttl=0.2)
    def wrapped(a, b):
        return mock_func()

    wrapped(1, 2)
    wrapped(1, 2)

    assert mock_func.call_count == 1

    time.sleep(0.3)
    wrapped(1, 2)
    time.sleep(0.3)
    wrapped(1, 2)

    assert mock_func.call_count == 3


def test_typed_false():
    mock_func = Mock(return_value="ok")

    @cache()
    def wrapped(a, b):
        return mock_func()

    wrapped(1, 2)
    wrapped(1.0, 2.0)

    assert mock_func.call_count == 1


def test_typed_true():
    mock_func = Mock(return_value="ok")

    @cache(typed=True)
    def wrapped(a, b):
        return mock_func()

    wrapped(1, 2)
    wrapped(1.0, 2.0)

    assert mock_func.call_count == 2
