from fun_language_package import fun_visitor, fun_utils


class FunctionArgumentIsFunctionDetector(fun_visitor.FunVisitor):
    def visit_fun_function_call(self, fun_function_call: fun_utils.FunFunctionCall) -> None:
        if isinstance(fun_function_call.fun_argument, fun_utils.FunFunction):
            raise fun_utils.EvaluationIsNotIntError(fun_function_call.fun_argument)

        super().visit_fun_function_call(fun_function_call)
