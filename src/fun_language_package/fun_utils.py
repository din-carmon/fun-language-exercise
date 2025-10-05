from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from fun_language_package import fun_visitor, function_argument_is_function_detector_visitor, \
    function_return_function_detector_visitor, unbound_variable_detector_visitor
from fun_language_package import evaluation_visitor


class EvalError(Exception):
    """Base class for evaluation-related errors."""
    pass


class UnboundVariableError(EvalError):
    def __init__(self, var_name: str) -> None:
        super().__init__(f"Unbound variable: {var_name}")
        self.var_name = var_name


class AlreadySubstitutedError(EvalError):
    def __init__(self, var_name: str) -> None:
        super().__init__(f"{var_name} is already substituted. Cannot substitute again")
        self.var_name = var_name


class FunctionEvaluationError(EvalError):
    def __init__(self, function: FunProgram) -> None:
        super().__init__(f"Function evaluation error: {function}. Cannot evaluate function type")
        self.function = function


class EvaluationIsNotIntError(EvalError):
    def __init__(self, evaluation: FunProgram) -> None:
        super().__init__(f"Evaluation is not an integer: {evaluation}")
        self.evaluation = evaluation


class FunProgram(ABC):

    @abstractmethod
    def accept(self, visitor: fun_visitor.FunVisitor) -> Any:
        pass


class FunInt(FunProgram):
    def __init__(self, value: int) -> None:
        self.value = value

    def accept(self, visitor: fun_visitor.FunVisitor) -> Any:
        return visitor.visit_fun_int(self)

    def __repr__(self) -> str:
        return f"{self.value}"


class FunPlusOperation(FunProgram):
    def __init__(self, left: FunProgram, right: FunProgram) -> None:
        self.left = left
        self.right = right

    def accept(self, visitor: fun_visitor.FunVisitor) -> Any:
        return visitor.visit_fun_plus_operation(self)

    def __repr__(self) -> str:
        return f"({self.left} + {self.right})"


class FunVar(FunProgram):
    def __init__(self, var_name: str) -> None:
        self.var_name = var_name

    def accept(self, visitor: fun_visitor.FunVisitor) -> Any:
        return visitor.visit_fun_var(self)

    def __repr__(self) -> str:
        return f"{self.var_name}"


class FunFunction(FunProgram):
    def __init__(self, fun_var: FunVar, fun_expression: FunProgram) -> None:
        self.fun_var = fun_var
        self.fun_expression = fun_expression

    def accept(self, visitor: fun_visitor.FunVisitor) -> Any:
        return visitor.visit_fun_function(self)

    def __repr__(self) -> str:
        return f"({self.fun_var}->{self.fun_expression})"


class FunFunctionCall(FunProgram):
    def __init__(self, function_expression: FunFunction, fun_argument: FunProgram) -> None:
        self.function_expression = function_expression
        self.fun_argument = fun_argument

    def accept(self, visitor: fun_visitor.FunVisitor) -> Any:
        return visitor.visit_fun_function_call(self)

    def __repr__(self) -> str:
        return f"({self.fun_argument} : {self.function_expression})"


def build_fun_program(program: tuple[Any, ...] | int | str) -> FunProgram:
    if isinstance(program, int):
        return FunInt(program)
    elif isinstance(program, str) and program not in {"+", "fun"}:
        return FunVar(program)
    elif isinstance(program, tuple):
        if len(program) == 3:
            if isinstance(program[0], str) and program[0] == "+":
                fun_program_1 = build_fun_program(program[1])
                fun_program_2 = build_fun_program(program[2])
                if isinstance(fun_program_1, FunFunction) or isinstance(fun_program_2, FunFunction):
                    raise TypeError(
                        f"Invalid addition of function with another program of any type: {fun_program_1}, {fun_program_2}")
                return FunPlusOperation(fun_program_1, fun_program_2)
            elif isinstance(program[0], str) and program[0] == "fun":
                fun_program_1 = build_fun_program(program[1])

                if not isinstance(fun_program_1, FunVar):
                    raise TypeError(f"Invalid function. First argument must be a variable: {fun_program_1}")

                fun_program_2 = build_fun_program(program[2])

                return FunFunction(fun_program_1, fun_program_2)
            else:
                raise TypeError(f"Invalid operator: {program[0]}")
        elif len(program) == 2:
            fun_program_1 = build_fun_program(program[0])
            fun_program_2 = build_fun_program(program[1])

            if not isinstance(fun_program_1, FunFunction):
                raise TypeError(f"Invalid function call. First argument must be a function: {fun_program_1}")
            return FunFunctionCall(fun_program_1, fun_program_2)
        else:
            raise TypeError(f"Invalid program: {program}")
    else:
        raise TypeError(f"Invalid program type: {type(program)}. Instance: {program}")


def evaluate(program: tuple[Any, ...] | int) -> int:
    fun_visitor = function_argument_is_function_detector_visitor.FunctionArgumentIsFunctionDetector()
    fun_visitor.visit(program)
    fun_visitor = function_return_function_detector_visitor.FunctionReturnFunctionDetectorVisitor()
    fun_visitor.visit(program)
    fun_visitor = unbound_variable_detector_visitor.UnboundVariableDetectorVisitor()
    fun_visitor.visit(program)
    fun_visitor = evaluation_visitor.EvaluationVisitor()
    return fun_visitor.visit(program)
