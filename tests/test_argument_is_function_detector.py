from __future__ import annotations
import pytest
from fun_language_package import fun_utils, function_argument_is_function_detector_visitor


def test_valid_function_argument() -> None:
    program = (("fun", "x", ("+", 1, "x")), 4)
    visitor = function_argument_is_function_detector_visitor.FunctionArgumentIsFunctionDetector()
    visitor.visit(program)


def test_invalid_function_argument() -> None:
    program = (("fun", "x", ("+", 1, "x")), ("fun", "x", ("+", 1, "x")))
    visitor = function_argument_is_function_detector_visitor.FunctionArgumentIsFunctionDetector()

    with pytest.raises(fun_utils.EvaluationIsNotIntError):
        visitor.visit(program)
