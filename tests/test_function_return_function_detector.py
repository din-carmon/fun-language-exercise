import pytest
from fun_language_package import fun_utils
from fun_language_package import function_return_function_detector_visitor


def test_valid_function_return() -> None:
    program = (("fun", "x", ("+", 1, "x")), 4)
    visitor = function_return_function_detector_visitor.FunctionReturnFunctionDetectorVisitor()
    visitor.visit(program)


def test_invalid_function_return() -> None:
    program = (("fun", "x", ("fun", "y", ("+", 1, "y"))), 4)
    visitor = function_return_function_detector_visitor.FunctionReturnFunctionDetectorVisitor()

    with pytest.raises(fun_utils.FunctionEvaluationError):
        visitor.visit(program)
