#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   __main__.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: frazanak <frazanak@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/29 10:51:45 by frazanak            #+#    #+#            #
#   Updated: 2026/11/02 13:00:39 by frazanak           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from typing import Any
import numpy
from .data_parsing import parse_functions_definition, parse_prompts
from llm_sdk import Small_LLM_Model  # type: ignore
from .fsm import FSM, FSMState
from .constrained import load_vocab, mask_logits


def build_system_prompt(user_prompt: str) -> str:
    definitions = parse_functions_definition()
    if not definitions:
        return user_prompt

    formatted_definitions: list[str] = []
    for definition in definitions:
        parameters = [
            f"{key}: {param.type}"
            for key, param in definition.parameters.items()
        ]
        params_str = ", ".join(parameters)
        formatted = (
            f"{definition.name}({params_str}) -> "
            f"{definition.returns.type}: {definition.description}"
        )
        formatted_definitions.append(formatted)

    functions_str = "\n".join(f"- {d}" for d in formatted_definitions)
    return (
        "You are a function calling assistant. "
        "Given a user request, respond with the correct function call.\n\n"
        f"Available functions:\n{functions_str}\n\n"
        f"User: {user_prompt}\n"
        "Assistant:"
    )


def emit_fixed(
    ids_array: list[int],
    model: Small_LLM_Model,
    text: str,
) -> None:
    fixed_ids = numpy.array(model.encode(text), copy=None)[0].tolist()
    ids_array.extend(fixed_ids)


def main() -> None:
    prompts = parse_prompts()
    if not prompts:
        return
    definitions = parse_functions_definition()
    if not definitions:
        return
    model = Small_LLM_Model()
    vocab_path: str = model.get_path_to_vocab_file()
    vocabs: dict[int, str] = load_vocab(vocab_path)
    for p in prompts:
        fsm = FSM(definitions)
        full_prompt = build_system_prompt(p.prompt)
        ids_array: list[int] = numpy.array(model.encode(full_prompt),
                                           copy=None)[0].tolist()

        emit_fixed(ids_array, model, ' {"name": "')

        for _ in range(10):
            if fsm.state != FSMState.NAME:
                break
            logits: list[float] = model.get_logits_from_input_ids(ids_array)
            valid_ids: list[int] = fsm.get_valid_ids(vocabs)
            masked: list[float] = mask_logits(logits, valid_ids)
            next_token: int = masked.index(max(masked))
            ids_array.append(next_token)
            fsm.feed(vocabs[next_token])

        if fsm.selected_func is None:
            print(f"[ERROR] could not identify function for: {p.prompt}")
            continue

        emit_fixed(ids_array, model, '", "parameters": {')

        param_dict: dict[str, Any] = {}
        while fsm.state != FSMState.END:
            param = fsm.get_current_param()
            param_type = fsm.get_current_param_type()
            max_token = 10 if param_type == 'number' else 30
            value: str = ""
            candidate_ids: list[int] = []

            emit_fixed(ids_array, model, f"\"{param}\": ")

            for _ in range(max_token):
                logits = model.get_logits_from_input_ids(ids_array)
                valid_ids = fsm.get_valid_ids(vocabs)
                masked = mask_logits(logits, valid_ids)
                next_token = masked.index(max(masked))
                ids_array.append(next_token)
                if param_type == "number":
                    token_str = vocabs[next_token]
                    value += token_str
                    try:
                        float(value)
                    except ValueError:
                        break
                if param_type == "string":
                    candidate_ids.append(next_token)
                    candidate_text = model.decode(candidate_ids)
                    if '"' in candidate_text:
                        parts = candidate_text.split('"')
                        if len(parts) == 3:
                            value = parts[1]
                            break
            if param_type == "number":
                param_dict[param] = float(value)
            if param_type == "string":
                param_dict[param] = value
            fsm.next_param()
            if fsm.state != FSMState.END:
                emit_fixed(ids_array, model, ", ")
        emit_fixed(ids_array, model, "}}")

        result = {
            "prompt": p.prompt,
            "name": fsm.selected_func.name,
            "parameters": param_dict
        }
        print(result)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] {e}")
    except (KeyboardInterrupt) as e:
        print(f"[INTERRUPTION ERROR] {e}")
