from dataclasses import dataclass, field, InitVar
from quick_actions import constants


@dataclass
class Display:
    show_tags: bool = True
    show_ids: bool = True
    show_prefixes: bool = True

    label_style: str = "{label}"
    id_style: str = constants.DEFAULT_PANDOC_ID_STYLE
    tag_style: str = constants.DEFAULT_PANDOC_TAG_STYLE
    tag_separator: str = constants.DEFAULT_PANDOC_TAG_SEPARATOR
    prefix_style: str = constants.DEFAULT_PANDOC_PREFIX_STYLE

    menu_prompt: str = constants.DEFAULT_MENU_PROMPT
