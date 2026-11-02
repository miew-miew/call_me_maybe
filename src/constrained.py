#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   learning.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: frazanak <frazanak@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/18 06:32:00 by frazanak            #+#    #+#            #
#   Updated: 2026/10/18 06:51:17 by frazanak           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import json


def load_vocab(path: str) -> dict[int, str]:
    with open(path) as file:
        content = file.read()
    vocabs = json.loads(content)
    return {v: k for k, v in vocabs.items()}


def mask_logits(
        logits: list[float],
        valid_ids: list[int]) -> list[float]:
    masked: list[float] = [-float("inf")] * len(logits)
    for id in valid_ids:
        masked[id] = logits[id]
    return masked
