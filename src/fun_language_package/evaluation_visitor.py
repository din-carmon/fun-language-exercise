from __future__ import annotations
from fun_language_package import fun_visitor, fun_utils
from typing import Any


class EvaluationVisitor(fun_visitor.FunVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.assignments: dict[str, fun_utils.FunProgram] = {}

    def visit(self, program: tuple[Any, ...] | int) -> int:
        fun_program = fun_utils.build_fun_program(program)
        self.assignments = {}
        evaluated = fun_program.accept(self)
        if not isinstance(evaluated, fun_utils.FunInt):
            raise fun_utils.EvaluationIsNotIntError(evaluated)

        return evaluated.value

    def visit_fun_int(self, fun_int: fun_utils.FunInt) -> fun_utils.FunInt:
        return fun_int

    def visit_fun_var(self, fun_var: fun_utils.FunVar) -> fun_utils.FunProgram:
        if self.assignments is not None and fun_var.var_name in self.assignments:
            return self.assignments[fun_var.var_name]

        # Otherwise, return a FunVar - We should not do anything else to simplify the expression.
        return fun_var

    def visit_fun_plus_operation(self, fun_plus_operation: fun_utils.FunPlusOperation) -> fun_utils.FunInt:
        left = fun_plus_operation.left.accept(self)
        right = fun_plus_operation.right.accept(self)

        if not isinstance(left, fun_utils.FunInt):
            raise fun_utils.EvaluationIsNotIntError(left)

        if not isinstance(right, fun_utils.FunInt):
            raise fun_utils.EvaluationIsNotIntError(right)

        return fun_utils.FunInt(left.value + right.value)

    def visit_fun_function(self, fun_function: fun_utils.FunFunction) -> fun_utils.FunFunction:
        return fun_function

    def visit_fun_function_call(self, fun_function_call: fun_utils.FunFunctionCall) -> fun_utils.FunInt:
        # 1. Evaluate the argument.
        argument = fun_function_call.fun_argument.accept(self)
        if not isinstance(argument, fun_utils.FunInt):
            raise TypeError(f"Invalid argument type: {type(argument)}. Instance: {argument}")

        # 2. Substitute the argument into the function expression, using updated assignments, and reevaluation.
        tmp_copy_of_current_assignments = self.assignments.copy()
        self.assignments[fun_function_call.function_expression.fun_var.var_name] = argument
        ret = fun_function_call.function_expression.fun_expression.accept(self)
        self.assignments = tmp_copy_of_current_assignments.copy() # Reset assignments

        if not isinstance(ret, fun_utils.FunInt):
            raise fun_utils.EvaluationIsNotIntError(ret)

        return ret
