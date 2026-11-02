#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   validation_errors.py                                 :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: frazanak <frazanak@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/01 09:49:34 by frazanak            #+#    #+#            #
#   Updated: 2026/10/01 10:12:17 by frazanak           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from pydantic import ValidationError


def print_validation_errors(e: ValidationError) -> None:
    errors = e.errors()
    for error in errors:
        if error["type"] == "extra_forbidden":
            field = error["loc"][-1]
            print(f"Additional fields such as '{field}'"
                  " are not permitted.")
        elif error["type"] == "missing":
            field = error["loc"][-1]
            usr_input = error["input"]
            print(f"The required '{field}' field is missing"
                  f" from the input: {usr_input}")
        else:
            print(error["msg"])
        # print(error)
