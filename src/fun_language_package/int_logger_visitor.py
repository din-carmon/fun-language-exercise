from fun_language_package import fun_utils, fun_visitor

class IntLogger(fun_visitor.FunVisitor):
    def visit_fun_int(self, fun_int: fun_utils.FunInt) -> None:
        print(fun_int.value)
