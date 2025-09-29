import pytest
from fun_language_package import fun_utils
from fun_language_package.fun_utils import evaluate


def test_int_for_program() -> None:
    assert fun_utils.evaluate(1) == 1


def test_valid_simple_tuple_for_program() -> None:
    assert fun_utils.evaluate(("+", 1, 2)) == 3


def test_nested_tuple_for_program() -> None:
    assert fun_utils.evaluate(("+", 1, ("+", 2, 3))) == 6


def test_invalid_type_for_program() -> None:
    with pytest.raises(TypeError, match=r"Invalid program type: <class 'list'>"):
        fun_utils.evaluate(["+", 2, 3])  # type: ignore[arg-type]


def test_invalid_tuple_size_for_program() -> None:
    with pytest.raises(TypeError, match=r"Invalid program type"):
        fun_utils.evaluate(("+", 1))


def test_invalid_operator_for_program() -> None:
    with pytest.raises(TypeError, match=r"Invalid operator: x"):
        fun_utils.evaluate(("x", 1, 2))


def test_invalid_nested_tuple_for_program() -> None:
    with pytest.raises(TypeError, match=r"Invalid operator: x"):
        fun_utils.evaluate(("+", 1, ("x", 2, 3)))


def test_fun_variable_construction() -> None:
    inst = fun_utils.build_fun_program("ABC")
    assert isinstance(inst, fun_utils.FunVar)
    assert inst.var_name == "ABC"


def test_fun_function_construction() -> None:
    inst = fun_utils.build_fun_program(("fun", "ABC", ("+", "ABC", 2)))
    assert isinstance(inst, fun_utils.FunFunction)
    assert inst.fun_var.var_name == "ABC"
    assert isinstance(inst.fun_expression, fun_utils.FunPlusOperation)
    assert isinstance(inst.fun_expression.left, fun_utils.FunVar)
    assert inst.fun_expression.left.var_name == "ABC"
    assert isinstance(inst.fun_expression.right, fun_utils.FunInt)
    assert inst.fun_expression.right.value == 2


def test_fun_function_call_construction() -> None:
    inst = fun_utils.build_fun_program((("fun", "ABC", ("+", "ABC", 2)), 2))
    assert isinstance(inst, fun_utils.FunFunctionCall)
    assert isinstance(inst.function_expression, fun_utils.FunFunction)
    assert inst.function_expression.fun_var.var_name == "ABC"
    assert isinstance(inst.fun_argument, fun_utils.FunInt)
    assert inst.fun_argument.value == 2


def test_fun_function_call_evaluation() -> None:
    inst = (("fun", "ABC", ("+", "ABC", 5)), 2)
    assert evaluate(inst) == 7


def test_fun_function_call_nested_variable_evaluation() -> None:
    inst = (("fun", "ABC", ("+", ("+", "ABC", 3), 4)), 2)
    assert evaluate(inst) == 9


def test_fun_function_call_nested_variable_twice_evaluation() -> None:
    inst = (("fun", "ABC", ("+", ("+", "ABC", 3), ("+", "ABC", 5))), 2)
    assert evaluate(inst) == 12


def test_addition_of_function_to_program() -> None:
    with pytest.raises(TypeError, match=r"Invalid addition of function"):
        fun_utils.build_fun_program(("+", ("fun", "ABC", ("+", "ABC", 2)), 3))


def test_function_call_argument_not_int() -> None:
    add_1 = ("fun", "x", ("+", "x", 1))
    add_2 = ("fun", "x", ("+", "x", 3))
    prog = (add_2, (add_1, 2))
    assert evaluate(prog) == 6


def test_function_call_argument_not_int_same_function() -> None:
    add_1 = ("fun", "x", ("+", "x", 1))
    prog = (add_1, (add_1, 2))
    assert evaluate(prog) == 4


def test_lambda_inside_lambda_with_same_parameter_name() -> None:
    add_1 = ("fun", "x", ("+", "x", 1))
    add_2 = ("fun", "x", (add_1, "x"))
    prog = (add_2, 1)
    assert evaluate(prog) == 2


def test_fun_program_as_input_to_fun_program() -> None:
    add_1 = ("fun", "x", ("+", "x", 1))
    add_2 = ("fun", "x", (add_1, (add_1, "x")))
    prog = (add_2, 2)
    assert evaluate(prog) == 4


def test_fun_program_as_input_to_fun_program2() -> None:
    add_1 = ("fun", "x", ("+", "x", 1))
    add_2 = ("fun", "y", (add_1, (add_1, "y")))
    prog = (add_2, 3)
    assert evaluate(prog) == 5

@pytest.mark.xfail(reason="Nested functions are not supported")
def test_nested_functions() -> None:
    add_1 = ("fun", "x", ("+", "x", "y"))
    add_2 = ("fun", "y", add_1)
    eval_1 = (add_2, 4)
    prog = (eval_1, 5)
    assert evaluate(prog) == 9

@pytest.mark.xfail(reason="Nested functions are not supported")
def test_same_var_nested_function() -> None:
    add_1 = ("fun", "x", ("+", "x", 0))
    add_2 = ("fun", "x", add_1)
    eval_1 = (add_2, 4)
    prog = (eval_1, 5)
    assert evaluate(prog) == 5
