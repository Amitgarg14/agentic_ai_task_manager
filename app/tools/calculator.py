def calculate(a: float, b: float, operation: str) -> float:
    """
    Perform a basic mathematical calculation.

    Args:
        a: First number.
        b: Second number.
        operation: Mathematical operation.

    Returns:
        The calculation result.

    Raises:
        ValueError: If the operation is unsupported or division by zero occurs.
    """

    if operation == "add":
        return a + b

    if operation == "subtract":
        return a - b

    if operation == "multiply":
        return a * b

    if operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b

    raise ValueError(f"Unsupported operation: {operation}")