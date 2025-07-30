import pytest
import logging
from typing import Callable
from unittest.mock import Mock, patch
from pydecora.decorators.suppress import suppress


def test_no_exception():
    mock_func = Mock(return_value="ok")

    @suppress(Exception)
    def wrapped():
        return mock_func()

    result = wrapped()

    assert result == "ok"


def test_matching_exception():
    mock_func = Mock(side_effect=ValueError("fail"))

    @suppress(ValueError, default_value="value")
    def wrapped():
        return mock_func()

    result = wrapped()

    assert result == "value"


def test_non_matching_exception():
    mock_func = Mock(side_effect=TypeError("fail"))

    @suppress(ValueError, default_value="value")
    def wrapped():
        return mock_func()

    with pytest.raises(TypeError, match="fail"):
        wrapped()


@patch("pydecora.decorators.suppress.logging.log")
def test_logging_enabled(mock_log: Callable):
    mock_func = Mock(side_effect=ValueError("fail"))

    @suppress(ValueError, default_value="value", log=True)
    def wrapped():
        return mock_func()

    wrapped()

    assert mock_log.call_args[1]["level"] == logging.INFO
    assert (
        mock_log.call_args[1]["msg"] == "fail was raised, returning default_value=value"
    )
