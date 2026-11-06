#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   data_loader.py                                       :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: frazanak <frazanak@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/29 10:50:26 by frazanak            #+#    #+#            #
#   Updated: 2026/11/03 08:37:09 by frazanak           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

def load_content(filepath: str) -> str | None:
    """Load and return the content of a file.

    Args:
        filepath: Path to the file.

    Returns:
        The file content, or None if an error occurs.
    """
    try:
        with open(filepath) as file:
            content = file.read()
    except OSError as e:
        print(e)
        return None
    return content
