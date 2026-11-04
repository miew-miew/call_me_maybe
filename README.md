*This project has been created as part of the 42 curriculum by frazanak.*

## Description

call me maybe is a function calling tool that translates natural language prompts into structured JSON function calls using a small LLM (Qwen3-0.6B).

Given a prompt like "What is the sum of 2 and 3?", the program outputs:

```json
{"name": "fn_add_numbers", "parameters": {"a": 2.0, "b": 3.0}}
```

The key idea is **constrained decoding**: instead of hoping the model generates valid JSON, we guide it token by token by masking out any token that would break the expected structure.

## Instructions

**Install dependencies:**

```bash
make install
```

**Run:**

```bash
uv run python -m src
```

**Lint:**

```bash
make lint
```

**Clean:**

```bash
make clean
```

## Algorithm Explanation

The generation is split into two phases, both using constrained decoding:

1. **Function name**: tokens are restricted to those that keep the accumulated string a valid prefix of a known function name. Once a full match is found, the FSM transitions to the next phase.
2. **Parameter values**: for each parameter, tokens are restricted based on the declared type — digits, `.` and `-` for numbers, anything for strings (until a closing `"` is detected).

At each step, invalid token logits are set to `-inf` before selecting the next token.

## Design Decisions

- A **Finite State Machine** (`FSM`) tracks the current generation phase and which parameter is being filled.
- **Pydantic** is used for all input/output validation.
- The vocabulary file is loaded once and reused across all prompts.
- Output directory is created automatically at write time.

## Performance Analysis

- Achieves near-perfect function selection and argument extraction on well-formed prompts.
- 100% valid JSON output guaranteed by construction.
- Processes all prompts in well under 5 minutes.

## Challenges Faced

The hardest part was designing the FSM — specifically deciding when to transition between states and how to handle partial token accumulation during function name matching.

The second challenge was knowing when to stop generating parameter values, especially for strings (detecting the closing quote across multiple tokens).

## Testing Strategy

blabla

## Example Usage

```bash
uv run python -m src
```

Output written to `data/output/function_calling_results.json`:

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

blabla

AI was used to help simplify docstrings across the codebase and to review and correct this README.
