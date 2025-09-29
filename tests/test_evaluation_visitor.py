from fun_language_package import evaluation_visitor


def test_evaluation_visitor_int_for_program() -> None:
    visitor = evaluation_visitor.EvaluationVisitor()

    assert visitor.visit(1) == 1


def test_evaluation_visitor_valid_simple_tuple_for_program() -> None:
    visitor = evaluation_visitor.EvaluationVisitor()
    assert visitor.visit(("+", 1, 2)) == 3


def test_evaluation_visitor_nested_tuple_for_program() -> None:
    visitor = evaluation_visitor.EvaluationVisitor()
    assert visitor.visit(("+", 1, ("+", 2, 3))) == 6

def test_evaluation_visitor_fun_function_call_evaluation() -> None:
    visitor = evaluation_visitor.EvaluationVisitor()
    inst = (("fun", "ABC", ("+", "ABC", 5)), 2)
    assert visitor.visit(inst) == 7


def test_evaluation_visitor_fun_function_call_nested_variable_evaluation() -> None:
    visitor = evaluation_visitor.EvaluationVisitor()
    inst = (("fun", "ABC", ("+", ("+", "ABC", 3), 4)), 2)
    assert visitor.visit(inst) == 9


def test_evaluation_visitor_fun_function_call_nested_variable_twice_evaluation() -> None:
    visitor = evaluation_visitor.EvaluationVisitor()
    inst = (("fun", "ABC", ("+", ("+", "ABC", 3), ("+", "ABC", 5))), 2)
    assert visitor.visit(inst) == 12


def test_evaluation_visitor_function_call_argument_not_int() -> None:
    visitor = evaluation_visitor.EvaluationVisitor()
    add_1 = ("fun", "x", ("+", "x", 1))
    add_2 = ("fun", "x", ("+", "x", 3))
    prog = (add_2, (add_1, 2))
    assert visitor.visit(prog) == 6


def test_evaluation_visitor_function_call_argument_not_int_same_function() -> None:
    visitor = evaluation_visitor.EvaluationVisitor()
    add_1 = ("fun", "x", ("+", "x", 1))
    prog = (add_1, (add_1, 2))
    assert visitor.visit(prog) == 4


def test_evaluation_visitor_lambda_inside_lambda_with_same_parameter_name() -> None:
    visitor = evaluation_visitor.EvaluationVisitor()
    add_1 = ("fun", "x", ("+", "x", 1))
    add_2 = ("fun", "x", (add_1, "x"))
    prog = (add_2, 1)
    assert visitor.visit(prog) == 2


def test_evaluation_visitor_fun_program_as_input_to_fun_program() -> None:
    visitor = evaluation_visitor.EvaluationVisitor()
    add_1 = ("fun", "x", ("+", "x", 1))
    add_2 = ("fun", "x", (add_1, (add_1, "x")))
    prog = (add_2, 2)
    assert visitor.visit(prog) == 4


def test_evaluation_visitor_fun_program_as_input_to_fun_program2() -> None:
    visitor = evaluation_visitor.EvaluationVisitor()
    add_1 = ("fun", "x", ("+", "x", 1))
    add_2 = ("fun", "y", (add_1, (add_1, "y")))
    prog = (add_2, 3)
    assert visitor.visit(prog) == 5
