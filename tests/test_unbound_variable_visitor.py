import pytest
from fun_language_package import fun_utils
from fun_language_package import unbound_variable_detector_visitor


def test_unbound_variable_detector_visitor_no_variables() -> None:
    program = ("+", 1, ("+", 2, 3))
    visitor = unbound_variable_detector_visitor.UnboundVariableDetectorVisitor()
    visitor.visit(program)


def test_unbound_variable_detector_visitor_one_variable() -> None:
    program = (("fun", "x", ("+", 1, "x")), 4)
    visitor = unbound_variable_detector_visitor.UnboundVariableDetectorVisitor()
    visitor.visit(program)


def test_unbound_variable_detector_visitor_two_variables() -> None:
    program = (("fun", "y", ("+", (("fun", "x", ("+", 1, "x")), 4), "y")), 3)
    visitor = unbound_variable_detector_visitor.UnboundVariableDetectorVisitor()
    visitor.visit(program)

def test_unbound_variable_detector_visitor_unbounded_variable() -> None:
    program = (("fun", "x", ("+", "y", "x")), 4)
    visitor = unbound_variable_detector_visitor.UnboundVariableDetectorVisitor()
    with pytest.raises(fun_utils.UnboundVariableError):
        visitor.visit(program)
