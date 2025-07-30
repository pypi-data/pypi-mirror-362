from dataclasses import dataclass
from quick_actions import constants


@dataclass
class Launcher:
    launcher_command: str | None = constants.DEFAULT_PROMPT
