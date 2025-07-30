# SPDX-FileCopyrightText: 2025 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: BSD-3-Clause

import gettext

from flowstrider.rules import attributes_dict, collections

# Constants:
# Maximum characters per line printed to the console
CMD_MAX_CHAR_WIDTH = 80
# Character width at which threat element names align right to and their content
# ...aligns left to
CMD_LEFT_CHAR_WIDTH = 25
# Colors:
C_HEADER = "\033[34m"
C_WARNING = "\033[31m"
C_DEFAULT = "\033[0m"


# System language that is being used for the system output on the command line
# ...like errors, warnings and tool status
lang_sys = gettext.translation("messages", localedir="localization", languages=["en"])
# Output language that is being used for the actual content (elicitation results (pdf
# ...and cmd) and metadata usage hints (xlsx))
lang_out = gettext.translation("messages", localedir="localization", languages=["en"])


def init_localization(language: str, position: str):
    """Manages the localization

    Args:
        language: the language string e.g.('en', 'de')
        position: whether to set the system language ('sys') or the output language
         ('out')

    """

    # Install gettext translation
    if position == "sys":
        global lang_sys
        lang_sys = gettext.translation(
            "messages", localedir="localization", languages=[language]
        )
        lang_sys.install()

    elif position == "out":
        global lang_out
        lang_out = gettext.translation(
            "messages", localedir="localization", languages=[language]
        )
        lang_out.install()

        # Update texts of rule collections, attributes and rules
        attributes_dict.init_attributes()
        all_rules = []
        for collection in collections.all_collections:
            collection.init_texts()
            all_rules.extend(collection.node_rules)
            all_rules.extend(collection.edge_rules)
            all_rules.extend(collection.dfd_rules)
            all_rules.extend(collection.graph_rules)
        for rule in all_rules:
            rule.init_texts()
