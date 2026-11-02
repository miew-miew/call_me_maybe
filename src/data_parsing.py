#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   data_parsing.py                                      :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: frazanak <frazanak@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/30 04:32:33 by frazanak            #+#    #+#            #
#   Updated: 2026/11/02 10:06:52 by frazanak           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from typing import TypeVar
from pydantic import TypeAdapter, ValidationError
from .data_loader import load_content
from .models import Prompt, FunctionDefinition
from .validation_errors import print_validation_errors


M = TypeVar('M', bound=Prompt | FunctionDefinition)


def parse_file(
    filepath: str,
    model: type[M]
) -> list[M] | None:
    content: str | None = load_content(filepath)
    if not content or content.strip() == '':
        print(f"No content found in {filepath}")
        return None
    adapter = TypeAdapter(list[M])
    try:
        return adapter.validate_json(content)
    except ValidationError as e:
        print_validation_errors(e)
        return None


def parse_prompts() -> list[Prompt] | None:
    return parse_file("data/input/function_calling_tests.json", Prompt)


def parse_functions_definition() -> list[FunctionDefinition] | None:
    return parse_file("data/input/functions_definition.json",
                      FunctionDefinition)
