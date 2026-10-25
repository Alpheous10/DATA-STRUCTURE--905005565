"""
DCOMP320 - Data Structures and Algorithms
Assignment: Stacks Implementation

Reads mathematical expressions from input.txt, evaluates each one using
stacks, and writes the results to output.txt in the same layout
(results replace expressions, separator lines are kept as they are).

Usage:
    python evaluator.py                      # uses input.txt -> output.txt
    python evaluator.py my_in.txt my_out.txt # custom file names
"""

import sys


# ---------------------------------------------------------------------------
# 1. Stack class
# ---------------------------------------------------------------------------
class Stack:
    """A simple LIFO (Last In, First Out) stack built on a Python list."""

    def __init__(self):
        self._items = []

    def push(self, item):
        """Add an item to the top of the stack."""
        self._items.append(item)

    def pop(self):
        """Remove and return the top item. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("pop from an empty stack")
        return self._items.pop()

    def peek(self):
        """Return the top item without removing it. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("peek at an empty stack")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)


# ---------------------------------------------------------------------------
# 2. Expression evaluation
# ---------------------------------------------------------------------------
PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2}


def tokenize(expression):
    """
    Break an expression string into tokens: numbers (as floats),
    operators (+ - * /) and parentheses.
    A minus sign counts as part of a number when it sits where a value is
    expected (start of expression, after "(" or after another operator),
    so "-3 + 10" and "2 * -3" both work.
    """
    tokens = []
    i = 0
    n = len(expression)

    while i < n:
        ch = expression[i]

        if ch.isspace():
            i += 1
            continue

        # Is the previous token something that produces a value?
        prev_is_value = bool(tokens) and (isinstance(tokens[-1], float) or tokens[-1] == ")")

        starts_number = ch.isdigit() or ch == "."
        starts_negative = (
            ch == "-"
            and not prev_is_value
            and i + 1 < n
            and (expression[i + 1].isdigit() or expression[i + 1] == ".")
        )

        if starts_number or starts_negative:
            start = i
            if starts_negative:
                i += 1
            while i < n and (expression[i].isdigit() or expression[i] == "."):
                i += 1
            text = expression[start:i]
            try:
                tokens.append(float(text))
            except ValueError:
                raise ValueError(f"Invalid number '{text}'")
        elif ch in "+-*/()":
            tokens.append(ch)
            i += 1
        else:
            raise ValueError(f"Invalid character '{ch}'")

    return tokens


def apply_operator(values, operators):
    """Pop one operator and two values, calculate, push the result back."""
    op = operators.pop()
    if values.size() < 2:
        raise ValueError("Malformed expression")

    right = values.pop()   # the second operand comes off the stack first
    left = values.pop()

    if op == "+":
        result = left + right
    elif op == "-":
        result = left - right
    elif op == "*":
        result = left * right
    else:  # "/"
        if right == 0:
            raise ZeroDivisionError("Division by zero")
        result = left / right

    values.push(result)


def evaluate(expression):
    """
    Evaluate an infix expression using two stacks:
      - values    : holds numbers
      - operators : holds operators and "("
    Precedence rule: before pushing a new operator, first apply any operator
    on top of the stack that has the same or higher precedence.
    """
    values = Stack()
    operators = Stack()
    expect_operand = True  # True when the next token must be a number or "("

    for token in tokenize(expression):
        if isinstance(token, float):
            if not expect_operand:
                raise ValueError("Missing operator between values")
            values.push(token)
            expect_operand = False

        elif token == "(":
            if not expect_operand:
                raise ValueError("Missing operator before '('")
            operators.push(token)

        elif token == ")":
            if expect_operand:
                raise ValueError("Unexpected ')'")
            while not operators.is_empty() and operators.peek() != "(":
                apply_operator(values, operators)
            if operators.is_empty():
                raise ValueError("Mismatched parentheses")
            operators.pop()  # discard the "("
            expect_operand = False

        else:  # + - * /
            if expect_operand:
                raise ValueError(f"Unexpected operator '{token}'")
            while (
                not operators.is_empty()
                and operators.peek() != "("
                and PRECEDENCE[operators.peek()] >= PRECEDENCE[token]
            ):
                apply_operator(values, operators)
            operators.push(token)
            expect_operand = True

    if expect_operand:
        raise ValueError("Expression is incomplete")

    while not operators.is_empty():
        if operators.peek() == "(":
            raise ValueError("Mismatched parentheses")
        apply_operator(values, operators)

    if values.size() != 1:
        raise ValueError("Malformed expression")

    return values.pop()


def format_result(value):
    """Show whole numbers without a decimal point (13 not 13.0)."""
    if value == int(value):
        return str(int(value))
    return str(round(value, 4))


# ---------------------------------------------------------------------------
# 3 & 4. File reading, evaluating and writing
# ---------------------------------------------------------------------------
def is_separator(line):
    """A separator is a line made only of dashes (at least three), e.g. -----"""
    line = line.strip()
    return len(line) >= 3 and set(line) == {"-"}


def process_file(input_path, output_path):
    """Read expressions, evaluate them, write results in the same layout."""
    with open(input_path, "r", encoding="utf-8-sig") as infile:
        lines = infile.read().splitlines()

    output_lines = []
    for line in lines:
        if not line.strip():
            continue  # ignore blank lines
        if is_separator(line):
            output_lines.append(line.strip())  # keep the same separator
            continue
        try:
            output_lines.append(format_result(evaluate(line)))
        except (ValueError, ZeroDivisionError, OverflowError) as error:
            output_lines.append(f"Error: {error}")

    with open(output_path, "w") as outfile:
        outfile.write("\n".join(output_lines) + "\n")


def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "output.txt"

    try:
        process_file(input_path, output_path)
    except FileNotFoundError:
        print(f"Could not find '{input_path}'. Put it in the same folder as this script.")
        return
    print(f"Done. Results written to {output_path}")


if __name__ == "__main__":
    main()
