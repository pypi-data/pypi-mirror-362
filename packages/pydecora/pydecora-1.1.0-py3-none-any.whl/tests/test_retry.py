import pytest
from typing import Callable
from unittest.mock import Mock, patch
from pydecora.decorators.retry import retry


def test_succeed_first_try():
    mock_func = Mock(return_value="ok")

    @retry(times=3)
    def wrapped():
        return mock_func()

    result = wrapped()
    assert result == "ok"
    assert mock_func.call_count == 1


def test_succeed_third_try():
    mock_func = Mock(side_effect=[Exception(), Exception(), "ok"])

    @retry(times=3)
    def wrapped():
        return mock_func()

    result = wrapped()
    assert result == "ok"
    assert mock_func.call_count == 3


def test_all_attempts_fail():
    mock_func = Mock(side_effect=Exception("fail"))

    @retry(times=3)
    def wrapped():
        return mock_func()

    with pytest.raises(Exception, match="fail"):
        wrapped()

    assert mock_func.call_count == 3


def test_custom_exception_filtering():
    mock_func = Mock(side_effect=[ValueError(), KeyError(), Exception("fail")])

    @retry(times=3, exceptions=(ValueError, KeyError))
    def wrapped():
        return mock_func()

    with pytest.raises(Exception, match="fail"):
        wrapped()

    assert mock_func.call_count == 3


@patch("time.sleep")
def test_delay_and_backoff(mock_sleep: Callable):
    mock_func = Mock(side_effect=[Exception(), Exception(), "ok"])

    @retry(times=3, delay=1, backoff_multiplier=2)
    def wrapped():
        return mock_func()

    result = wrapped()

    assert result == "ok"
    assert mock_func.call_count == 3
    assert mock_sleep.call_args_list == [((1,),), ((2,),)]


def test_callback():
    mock_func = Mock(side_effect=[Exception("fail"), "ok"])
    mock_callback = Mock()

    @retry(times=3, callback=mock_callback)
    def wrapped():
        return mock_func()

    result = wrapped()

    assert result == "ok"
    assert mock_func.call_count == 2
    assert mock_callback.call_count == 1
    assert mock_callback.call_args[0][0] == 1
    assert isinstance(mock_callback.call_args[0][1], Exception)
    assert str(mock_callback.call_args[0][1]) == "fail"
