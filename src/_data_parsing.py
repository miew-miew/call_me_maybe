#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   _data_parsing.py                                     :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: frazanak <frazanak@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/30 04:32:33 by frazanak            #+#    #+#            #
#   Updated: 2026/11/08 12:18:24 by frazanak           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import json
from typing import Any
from pydantic import ValidationError
from ._data_loader import load_content
from ._models import Prompt, FunctionDefinition
from ._validation_errors import print_validation_errors


def parse_file(filepath: str) -> Any | None:
    """Load and decode a JSON file.

    Args:
        filepath: Path to the JSON file.

    Returns:
        The parsed list, or None if loading or decoding fails.
    """
    content: str | None = load_content(filepath)
    if not content or content.strip() == '':
        return None
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {filepath}: {e}")
        return None


def parse_prompts() -> list[Prompt] | None:
    """Parse the prompts from the JSON file, skipping invalid entries.

    Returns:
        The list of valid prompts, or None if the file cannot be loaded.
    """
    filepath = "data/input/function_calling_tests.json"
    raw = parse_file(filepath)
    if raw is None or len(raw) == 0:
        print("No available prompt.")
        return None
    valid: list[Prompt] = []
    for item in raw:
        try:
            valid.append(Prompt.model_validate(item))
        except ValidationError as e:
            print_validation_errors(e, filepath)
            print("[ERROR] Skipping invalid prompt.")
    return valid or None


def parse_functions_definition() -> list[FunctionDefinition] | None:
    """Parse the function definitions from the JSON file.

    Returns:
        The list of function definitions, or None if parsing fails.
    """
    filepath = "data/input/functions_definition.json"
    raw = parse_file(filepath)
    if raw is None or len(raw) == 0:
        print("No available function definition.")
        return None
    try:
        return [FunctionDefinition.model_validate(item) for item in raw]
    except ValidationError as e:
        print_validation_errors(e, filepath)
        return None
