

def evaluate(program: tuple | int):
    if isinstance(program, tuple):
        if len(program) != 3:
            raise TypeError(f"Invalid program: {program}")
        if not isinstance(program[0], str) or program[0] not in ["+"]:
            raise TypeError(f"Invalid operator: {program[0]}")

        return evaluate(program[1]) + evaluate(program[2])
    elif isinstance(program, int):
        return program
    else:
        raise TypeError(f"Invalid program type: {type(program)}. Instance: {program}")
