#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   constrained.py                                       :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: frazanak <frazanak@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/10/18 06:32:00 by frazanak            #+#    #+#            #
#   Updated: 2026/11/03 08:32:15 by frazanak           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import json


def load_vocab(path: str) -> dict[int, str]:
    """Load the vocabulary file and map token IDs to tokens.

    Args:
        path (str): The path to the vocabulary file.

    Returns:
        dict[int, str]: A dictionary mapping token IDs to tokens.
    """
    with open(path) as file:
        content = file.read()
    vocabs = json.loads(content)
    return {v: k for k, v in vocabs.items()}


def mask_logits(
    logits: list[float],
    valid_ids: list[int]
) -> list[float]:
    """Mask the logits of invalid tokens with negative infinity.

    Args:
        logits (list[float]): The logits for each token.
        valid_ids (list[int]): The IDs of valid tokens.

    Returns:
        list[float]: The logits with invalid tokens masked.
    """
    masked: list[float] = [-float("inf")] * len(logits)
    for id in valid_ids:
        masked[id] = logits[id]
    return masked
