from fun_language_package import fun_utils
from fun_language_package.fun_utils import UnboundVariableError
from fun_language_package import fun_visitor
from typing import Any


class UnboundVariableDetectorVisitor(fun_visitor.FunVisitor):
    """
    A visitor that raises an error if the program contains an unbound variable (i.e., a variable p
    that's not inside a Fun function
    """
    def __init__(self) -> None:
        super().__init__()
        self.bounded_variables: set[str] = set()

    def visit(self, program: tuple[Any, ...] | int) -> None:
        self.bounded_variables = set()
        super().visit(program)

    def visit_fun_var(self, fun_var: fun_utils.FunVar) -> None:
        if fun_var.var_name not in self.bounded_variables:
            raise UnboundVariableError(fun_var.var_name)

    def visit_fun_function(self, fun_function: fun_utils.FunFunction) -> None:
        fun_function.fun_expression.accept(self)
        # Intentionally not visiting function variable instance
        # fun_function.fun_var.accept(self)

    def visit_fun_function_call(self, fun_function_call: fun_utils.FunFunctionCall) -> None:
        # 1. Verify that the argument has no unbound variables in its expression.
        fun_function_call.fun_argument.accept(self)

        # 2. Add the new assignment and continue visiting and checking for unbound variables.
        bounded_variables_copy = self.bounded_variables.copy()
        self.bounded_variables.add(fun_function_call.function_expression.fun_var.var_name)

        try:
            fun_function_call.function_expression.accept(self)
        finally:
            self.bounded_variables = bounded_variables_copy
