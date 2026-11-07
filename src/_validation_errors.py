#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   _validation_errors.py                                :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: frazanak <frazanak@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/01 09:49:34 by frazanak            #+#    #+#            #
#   Updated: 2026/11/07 15:25:40 by frazanak           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from pydantic import ValidationError


def print_validation_errors(e: ValidationError, filepath: str) -> None:
    """Print human-readable messages from a pydantic ValidationError.

    Args:
        e: The ValidationError to format and print.
    """
    errors = e.errors()
    for error in errors:
        if error["type"] == "extra_forbidden":
            field = error["loc"][-1]
            print(f"Additional fields such as '{field}'"
                  " are not permitted.")
            print(f"Filepath: {filepath}")
        elif error["type"] == "missing":
            field = error["loc"][-1]
            usr_input = error["input"]
            print(f"The required '{field}' field is missing"
                  f" from the input: {usr_input}")
            print(f"Filepath: {filepath}")
        else:
            field = error["loc"][-1]
            print(f"{field}: {error['msg']}")
            print(f"Filepath: {filepath}")
