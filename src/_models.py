#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   _models.py                                           :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: frazanak <frazanak@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/29 10:05:11 by frazanak            #+#    #+#            #
#   Updated: 2026/11/08 12:00:11 by frazanak           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Literal


class Prompt(BaseModel):
    """A user prompt input model."""

    prompt: str = Field(...)
    model_config = ConfigDict(extra="forbid")


class ParamType(BaseModel):
    """A parameter type descriptor."""

    type: Literal["number", "string"]
    model_config = ConfigDict(extra="forbid")


class FunctionDefinition(BaseModel):
    """A callable function definition with its parameters and return type."""

    name: str = Field(..., min_length=5)
    description: str = Field(..., min_length=5)
    parameters: dict[str, ParamType] = Field(...)
    returns: ParamType = Field(...)
    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def check_param_names(self) -> "FunctionDefinition":
        """Ensure no parameter name is an empty string."""
        for key in self.parameters:
            if key.strip() == "":
                raise Exception("parameters name shouldn't be empty.")
        return self


class OutputValidator(BaseModel):
    """Validates the output of a function call prediction."""

    prompt: str
    name: str
    parameters: dict[str, float | str]
    model_config = ConfigDict(extra="forbid")
