from fun_language_package import int_logger_visitor
from _pytest.capture import CaptureFixture


def test_int_logger_visitor(capsys: CaptureFixture[str]) -> None:
    program = ("+", 1, ("+", 2, 3))
    visitor = int_logger_visitor.IntLogger()
    visitor.visit(program)
    captured = capsys.readouterr()
    assert captured.out == ("1\n2\n3\n")
