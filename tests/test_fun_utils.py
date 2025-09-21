import pytest
from fun_language_package import fun_utils


def test_int_for_program():
    assert 1 == fun_utils.evaluate(1)


def test_valid_simple_tuple_for_program():
    assert 3 == fun_utils.evaluate(("+", 1, 2))


def test_nested_tuple_for_program():
    assert 6 == fun_utils.evaluate(("+", 1, ("+", 2, 3)))


def test_invalid_type_for_program():
    with pytest.raises(TypeError, match=r"Invalid program type: <class 'list'>"):
        fun_utils.evaluate(["+", 2, 3])


def test_invalid_tuple_size_for_program():
    with pytest.raises(TypeError, match=r"Invalid program:"):
        fun_utils.evaluate(("+", 1))


def test_invalid_operator_for_program():
    with pytest.raises(TypeError, match=r"Invalid operator: x"):
        fun_utils.evaluate(("x", 1, 2))


def test_invalid_nested_tuple_for_program():
    with pytest.raises(TypeError, match=r"Invalid operator: x"):
        fun_utils.evaluate(("+", 1, ("x", 2, 3)))