#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   models.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: frazanak <frazanak@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/29 10:05:11 by frazanak            #+#    #+#            #
#   Updated: 2026/10/18 07:57:18 by frazanak           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from pydantic import BaseModel, Field, ConfigDict
from typing import Literal


class Prompt(BaseModel):
    prompt: str = Field(...)
    model_config = ConfigDict(extra="forbid")


class ParamType(BaseModel):
    type: Literal["number", "string"]
    model_config = ConfigDict(extra="forbid")


class FunctionDefinition(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    parameters: dict[str, ParamType] = Field(...)
    returns: ParamType = Field(...)
    model_config = ConfigDict(extra="forbid")


class OutputValidator(BaseModel):
    prompt: str
    name: str
    parameters: dict[str, float | str]
    model_config = ConfigDict(extra="forbid")

