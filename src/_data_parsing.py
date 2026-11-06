#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   _data_parsing.py                                     :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: frazanak <frazanak@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/30 04:32:33 by frazanak            #+#    #+#            #
#   Updated: 2026/11/06 13:15:28 by frazanak           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import json
from typing import TypeVar
from pydantic import TypeAdapter, ValidationError
from ._data_loader import load_content
from ._models import Prompt, FunctionDefinition
from ._validation_errors import print_validation_errors


M = TypeVar('M', bound=Prompt | FunctionDefinition)


def parse_file(
    filepath: str,
    model: type[M],
    skip_invalid: bool = False,
) -> list[M] | None:
    """Parse a JSON file into a list of model instances.

    Args:
        filepath: Path to the JSON file.
        model: The model class used for validation.
        skip_invalid: If True, skip invalid entries instead of failing.

    Returns:
        The validated list of models, or None if parsing fails.
    """
    content: str | None = load_content(filepath)
    if not content or content.strip() == '':
        print(f"No content found in {filepath}")
        return None
    if not skip_invalid:
        adapter = TypeAdapter(list[M])
        try:
            return adapter.validate_json(content)
        except ValidationError as e:
            print_validation_errors(e)
            return None
    item_adapter = TypeAdapter(model)
    valid: list[M] = []
    for item in json.loads(content):
        try:
            valid.append(item_adapter.validate_python(item))
        except ValidationError as e:
            print_validation_errors(e)
            print("[ERROR] Skipping invalid entry")
    return valid or None


def parse_prompts() -> list[Prompt] | None:
    """Parse the prompts from the JSON file, skipping invalid entries.

    Returns:
        The list of valid prompts, or None if the file cannot be loaded.
    """
    return parse_file(
        "data/input/function_calling_tests.json", Prompt, skip_invalid=True
    )


def parse_functions_definition() -> list[FunctionDefinition] | None:
    """Parse the function definitions from the JSON file.

    Returns:
        The list of function definitions, or None if parsing fails.
    """
    return parse_file("data/input/functions_definition.json",
                      FunctionDefinition)
