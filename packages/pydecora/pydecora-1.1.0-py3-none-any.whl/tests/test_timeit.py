import re
import logging
import pytest
from typing import Callable
from unittest.mock import Mock, patch
from pydecora.decorators.timeit import timeit


@patch("logging.log")
def test_no_parameters(mock_log: Callable):

    @timeit()
    def wrapped():
        pass

    wrapped()

    cleaned = re.sub(r"\d+\.\d+", "", mock_log.call_args[0][1])

    assert mock_log.call_args[0][0] == logging.INFO
    assert cleaned == "wrapped() took s"


@patch("logging.log")
def test_label(mock_log: Callable):

    @timeit(label="test_func")
    def wrapped():
        pass

    wrapped()

    cleaned = re.sub(r"\d+\.\d+", "", mock_log.call_args[0][1])

    assert mock_log.call_args[0][0] == logging.INFO
    assert cleaned == "test_func() took s"


@patch("logging.log")
def test_log_args(mock_log: Callable):

    @timeit(log_args=True)
    def wrapped(a, b, *, c):
        pass

    wrapped(10, 20, c=30)

    cleaned = re.sub(r"\d+\.\d+", "", mock_log.call_args[0][1])

    assert mock_log.call_args[0][0] == logging.INFO
    assert cleaned == "wrapped(10, 20, c=30) took s"


@patch("logging.log")
def test_log_args_no_args(mock_log: Callable):

    @timeit(log_args=True)
    def wrapped():
        pass

    wrapped()

    cleaned = re.sub(r"\d+\.\d+", "", mock_log.call_args[0][1])

    assert mock_log.call_args[0][0] == logging.INFO
    assert cleaned == "wrapped() took s"


@patch("logging.log")
def test_log_result(mock_log: Callable):

    @timeit(log_result=True)
    def wrapped():
        return "ok"

    wrapped()

    cleaned = re.sub(r"\d+\.\d+", "", mock_log.call_args[0][1])

    assert mock_log.call_args[0][0] == logging.INFO
    assert cleaned == "wrapped() took s and returned: \n ok"


@patch("logging.log")
def test_log_level(mock_log: Callable):

    @timeit(log_level=logging.DEBUG)
    def wrapped():
        pass

    wrapped()

    cleaned = re.sub(r"\d+\.\d+", "", mock_log.call_args[0][1])

    assert mock_log.call_args[0][0] == logging.DEBUG
    assert cleaned == "wrapped() took s"


@patch("logging.log")
def test_unit(mock_log: Callable):

    @timeit(unit="ms")
    def wrapped():
        pass

    wrapped()

    cleaned = re.sub(r"\d+\.\d+", "", mock_log.call_args[0][1])

    assert mock_log.call_args[0][0] == logging.INFO
    assert cleaned == "wrapped() took ms"


def test_unit_unknown():

    @timeit(unit="unknown")
    def wrapped():
        return "ok"

    with pytest.raises(ValueError, match="'unknown' is an unknown unit"):
        wrapped()
