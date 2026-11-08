*This project has been created as part of the 42 curriculum by frazanak.*

## Description

call me maybe translates natural language prompts into structured JSON function calls using a small LLM (Qwen3-0.6B) and constrained decoding.

Given "What is the sum of 2 and 3?", it produces:

```json
{"name": "fn_add_numbers", "parameters": {"a": 2.0, "b": 3.0}}
```

## Instructions

```bash
make install
uv run python -m src
```

## Algorithm Explanation

Generation happens in two phases:

1. Function name: only tokens that extend the current string toward a valid function name are allowed.
2. Parameter values: tokens are restricted by type — numbers only accept digits, `.` and `-`; strings accept anything until a closing `"` is detected.

At each step, invalid tokens are masked to `-inf` so the model can only pick valid ones.

## Design Decisions

- A Finite State Machine (FSM) tracks the current phase (NAME, PARAM_VALUE, END).
- Pydantic validates all inputs and outputs. Invalid prompts are skipped individually.
- The output directory is created after running the program.

## Performance Analysis

- Near-perfect accuracy on well-formed prompts.
- 100% valid JSON guaranteed by construction.
- Runs all prompts in under 5 minutes on standard hardware.
- No crash — all errors are caught and printed.

## Challenges Faced

The hardest part was designing the FSM, especially understanding what states were needed and what each state should do.

The second challenge was deciding when to stop generating parameter values — detecting an invalid float mid-stream for numbers, and finding the closing quote across multiple tokens for strings.

## Testing Strategy

Tested with different cases: missing files, invalid function definitions, and prompts that don't match any function.

## Example Usage

```bash
uv run python -m src
```

Results are written to `data/output/function_calling_results.json`.
```json
[
  {
    "prompt": "What is the sum of 2 and 3?",
    "name": "fn_add_numbers",
    "parameters": {"a": 2.0, "b": 3.0}
  },
  {
    "prompt": "Reverse the string 'hello'",
    "name": "fn_reverse_string",
    "parameters": {"s": "hello"}
  }
]
```

## Resources

- [Pydantic docs](https://docs.pydantic.dev/)
- [uv – Python Package Manager](https://docs.astral.sh/uv/)
- [Constrained decoding](https://mbrenndoerfer.com/writing/constrained-decoding-structured-llm-output)

AI was used to simplify docstrings, review this README, and provide suggestions for code refactoring.
