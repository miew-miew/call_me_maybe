#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   data_loader.py                                       :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: frazanak <frazanak@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/09/29 10:50:26 by frazanak            #+#    #+#            #
#   Updated: 2026/09/30 14:17:58 by frazanak           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

def load_content(filepath: str) -> str | None:
    try:
        with open(filepath) as file:
            content = file.read()
    except OSError as e:
        print(e)
        return None
    return content
