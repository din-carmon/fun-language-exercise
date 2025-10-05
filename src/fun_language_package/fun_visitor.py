from __future__ import annotations
from fun_language_package import fun_utils
from typing import Any


class FunVisitor:
    def visit(self, program: tuple[Any, ...] | int) -> Any:
        fun_program = fun_utils.build_fun_program(program)
        return fun_program.accept(self)

    def visit_fun_int(self, fun_int: fun_utils.FunInt) -> Any:
        pass

    def visit_fun_var(self, fun_var: fun_utils.FunVar) -> Any:
        pass

    def visit_fun_plus_operation(self, fun_plus_operation: fun_utils.FunPlusOperation) -> Any:
        fun_plus_operation.left.accept(self)
        fun_plus_operation.right.accept(self)

    def visit_fun_function(self, fun_function: fun_utils.FunFunction) -> Any:
        fun_function.fun_expression.accept(self)
        fun_function.fun_var.accept(self)

    def visit_fun_function_call(self, fun_function_call: fun_utils.FunFunctionCall) -> Any:
        fun_function_call.function_expression.accept(self)
        fun_function_call.fun_argument.accept(self)
