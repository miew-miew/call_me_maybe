#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   _data_parsing.py                                     :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: frazanak <frazanak@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/30 04:32:33 by frazanak            #+#    #+#            #
#   Updated: 2026/11/07 15:32:32 by frazanak           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import json
from typing import TypeVar
from pydantic import BaseModel, ValidationError
from ._data_loader import load_content
from ._models import Prompt, FunctionDefinition
from ._validation_errors import print_validation_errors


M = TypeVar('M', bound=BaseModel)


def parse_file(
    filepath: str,
    model: type[M],
    skip_invalid: bool = False,
    show_skip_warning: bool = False,
) -> list[M] | None:
    """Parse a JSON file into a list of model instances.

    Args:
        filepath: Path to the JSON file.
        model: The model class used for validation.
        skip_invalid: If True, skip invalid entries instead of failing.
        show_skip_warning: Whether to print the skip notice for invalid
            entries.

    Returns:
        The validated list of models, or None if parsing fails.
    """
    content: str | None = load_content(filepath)
    if not content or content.strip() == '':
        print(f"No content found in {filepath}")
        return None

    try:
        payload = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in {filepath}: {e}")
        return None

    if not skip_invalid:
        try:
            return [model.model_validate(item) for item in payload]
        except ValidationError as e:
            print_validation_errors(e, filepath)
            return None

    valid: list[M] = []
    for item in payload:
        try:
            valid.append(model.model_validate(item))
        except ValidationError as e:
            print_validation_errors(e, filepath)
            if show_skip_warning:
                print("[ERROR] Skipping invalid entry")
    return valid or None


def parse_prompts() -> list[Prompt] | None:
    """Parse the prompts from the JSON file, skipping invalid entries.

    Returns:
        The list of valid prompts, or None if the file cannot be loaded.
    """
    return parse_file(
        "data/input/function_calling_tests.json",
        Prompt,
        skip_invalid=True,
        show_skip_warning=True,
    )


def parse_functions_definition() -> list[FunctionDefinition] | None:
    """Parse the function definitions from the JSON file.

    Returns:
        The list of function definitions, or None if parsing fails.
    """
    return parse_file(
        "data/input/functions_definition.json",
        FunctionDefinition
    )
