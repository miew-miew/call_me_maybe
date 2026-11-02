#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   fsm.py                                               :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: frazanak <frazanak@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: Invalid date        by                     #+#    #+#            #
#   Updated: 2026/10/26 07:46:51 by frazanak           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from enum import Enum
from .models import FunctionDefinition


class FSMState(Enum):
    NAME = "name"
    PARAM_VALUE = "param_value"
    END = "end"


class FSM:
    def __init__(self, definitions: list[FunctionDefinition]) -> None:
        self.state = FSMState.NAME
        self.definitions = definitions
        self.selected_func: FunctionDefinition | None = None
        self._params: list[str] = []
        self._current_param_pos = 0
        self._accumulated_name: str = ""

    def set_function(self, name: str) -> bool:
        for func in self.definitions:
            if name == func.name:
                self.selected_func = func
                self._params = list(func.parameters.keys())
                self.state = FSMState.PARAM_VALUE
                return True
        return False

    def get_current_param(self) -> str:
        return self._params[self._current_param_pos]

    def get_current_param_type(self) -> str | None:
        if self.state != FSMState.PARAM_VALUE or not self.selected_func:
            return None
        param = self.get_current_param()
        return self.selected_func.parameters[param].type

    def next_param(self) -> None:
        self._current_param_pos += 1
        if self._current_param_pos == len(self._params):
            self.state = FSMState.END

    def get_valid_ids(
            self,
            vocabs: dict[int, str]
    ) -> list[int]:
        valid_ids: list[int] = []
        if self.state == FSMState.NAME:
            functions = [d.name for d in self.definitions]
            for token_id, token_str in vocabs.items():
                candidate = self._accumulated_name + token_str
                for function in functions:
                    if function.startswith(candidate):
                        valid_ids.append(token_id)
                        break
            return valid_ids
        if self.state == FSMState.PARAM_VALUE:
            param_type = self.get_current_param_type()
            if param_type == "number":
                for token_id, token_str in vocabs.items():
                    if token_str in (".", "-"):
                        valid_ids.append(token_id)
                    else:
                        try:
                            if float(token_str).is_integer():
                                valid_ids.append(token_id)
                        except ValueError:
                            pass
                return valid_ids
            else:
                return list(vocabs.keys())
        return []

    def feed(self, token_str: str) -> None:
        if self.state == FSMState.NAME:
            self._accumulated_name += token_str
            if self.set_function(self._accumulated_name):
                self._accumulated_name = ""
