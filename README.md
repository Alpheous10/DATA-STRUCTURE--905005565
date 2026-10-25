
A Python program that reads maths expressions from `input.txt`, evaluates each one using stacks, and writes the answers to `output.txt`.

## How to run

1. Install Python 3 (no extra libraries are needed).
2. Put `evaluator.py` and `input.txt` in the same folder.
3. Open a terminal in that folder and run:

```
python evaluator.py
```

4. Open `output.txt` to see the results.

You can also pass your own file names: `python evaluator.py my_input.txt my_output.txt`

## Input format

- One expression per line.
- Expressions are separated by a line made only of dashes (for example `-----`).
- Supported: `+  -  *  /`, parentheses, decimals, negative numbers, and spaces between tokens.

```
3 + 5 * 2
-----
(8 / 4) + 7 * 2
```

## Output format

Same layout as the input. Each expression is replaced by its result and the separator lines are copied unchanged.

```
13
-----
16
```

Whole-number results are shown without a decimal point. Other results are rounded to 4 decimal places (`7 / 2` gives `3.5`).

## How it works

- `Stack` class: `push`, `pop`, `peek`, `is_empty`, `size`.
- `evaluate()` uses two stacks, one for numbers and one for operators. Higher-precedence operators (`*`, `/`) are applied before lower ones (`+`, `-`), and parentheses force their contents to be evaluated first.
- `process_file()` reads the input, evaluates line by line, and writes the output.

## Error handling

A bad expression does not stop the program. Its line in `output.txt` shows an error message and the program carries on with the rest.

| Problem | Output |
|---|---|
| Division by zero | `Error: Division by zero` |
| Missing bracket | `Error: Mismatched parentheses` |
| Misplaced operator | `Error: Unexpected operator '*'` |
| Unknown character | `Error: Invalid character '$'` |

## Assumptions and limitations

- A line made only of three or more dashes is treated as a separator.
- Blank lines are ignored.
- Each expression sits on a single line.
- A negative sign is supported directly in front of a number (`-3`, `2 * -3`) but not in front of brackets (`-(2 + 3)`).
- Exponents (`^`), functions and variables are not supported.
- The sample output in the assignment sheet shows 17 for `(8 / 4) + 7 * 2`. The correct answer is 16 (2 + 14), and this program gives 16.
