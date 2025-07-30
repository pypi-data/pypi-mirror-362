import pytest
from unittest.mock import Mock
from pydecora.decorators.validate_args import validate_args
from typing import List, Dict, Tuple, Optional, Union


def test_valid_args():
    mock_func = Mock(return_value="ok")

    @validate_args()
    def wrapped(a: int, b: str):
        return mock_func()

    wrapped(1, "x")
    assert mock_func.call_count == 1


def test_invalid_arg_type():
    mock_func = Mock()

    @validate_args()
    def wrapped(a: int):
        return mock_func()

    with pytest.raises(TypeError):
        wrapped("not an int")


def test_return_type_passes():
    mock_func = Mock(return_value="ok")

    @validate_args(check_return=True)
    def wrapped() -> str:
        return mock_func()

    wrapped()
    assert mock_func.call_count == 1


def test_return_type_fails():
    mock_func = Mock(return_value=123)

    @validate_args(check_return=True)
    def wrapped() -> str:
        return mock_func()

    with pytest.raises(TypeError):
        wrapped()


def test_union_valid():
    mock_func = Mock()

    @validate_args()
    def wrapped(x: Union[int, str]):
        return mock_func()

    wrapped(42)
    wrapped("hi")
    assert mock_func.call_count == 2


def test_union_invalid():
    mock_func = Mock()

    @validate_args()
    def wrapped(x: Union[int, str]):
        return mock_func()

    with pytest.raises(TypeError):
        wrapped(3.14)


def test_tuple_fixed_valid():
    mock_func = Mock()

    @validate_args()
    def wrapped(x: Tuple[int, str]):
        return mock_func()

    wrapped((1, "a"))
    assert mock_func.call_count == 1


def test_tuple_fixed_invalid():
    mock_func = Mock()

    @validate_args()
    def wrapped(x: Tuple[int, str]):
        return mock_func()

    with pytest.raises(TypeError):
        wrapped((1, 2))


def test_tuple_variable_length():
    mock_func = Mock()

    @validate_args()
    def wrapped(x: Tuple[int, ...]):
        return mock_func()

    wrapped((1, 2, 3))
    assert mock_func.call_count == 1


def test_nested_dict_list_valid():
    mock_func = Mock()

    @validate_args()
    def wrapped(x: List[Dict[str, Optional[int]]]):
        return mock_func()

    wrapped([{"a": 1}, {"b": None}])
    assert mock_func.call_count == 1


def test_nested_dict_list_invalid():
    mock_func = Mock()

    @validate_args()
    def wrapped(x: List[Dict[str, Optional[int]]]):
        return mock_func()

    with pytest.raises(TypeError):
        wrapped([{"a": "bad"}])


def test_exclusion_skips_check():
    mock_func = Mock()

    @validate_args(exclusions=["ignore"])
    def wrapped(a: int, ignore):
        return mock_func()

    wrapped(5, "not checked")
    assert mock_func.call_count == 1


def test_warn_only_logs(caplog):
    mock_func = Mock()

    @validate_args(warn_only=True)
    def wrapped(x: int):
        return mock_func()

    caplog.set_level("WARNING")
    wrapped("bad")

    assert "x failed type check" in caplog.text
    assert mock_func.call_count == 1
