from __future__ import annotations
from fun_language_package import fun_utils, fun_visitor


class FunctionReturnFunctionDetectorVisitor(fun_visitor.FunVisitor):
    """
    A visitor that raises an error if the program contains a function that returns a function instead
    of an integer.
    """
    def visit_fun_function(self, fun_function: fun_utils.FunFunction) -> None:
        if isinstance(fun_function.fun_expression, fun_utils.FunFunction):
            raise fun_utils.FunctionEvaluationError(fun_function)

        fun_function.fun_expression.accept(self)
