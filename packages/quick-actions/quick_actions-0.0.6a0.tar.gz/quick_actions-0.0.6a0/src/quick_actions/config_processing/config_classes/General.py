from dataclasses import dataclass, field, InitVar
from typing import List, Dict

from quick_actions.config_processing.config_classes.Launcher import Launcher
from quick_actions.config_processing.config_classes.Display import Display


@dataclass
class General:
    disabled_units: List[str] | None = None

    display_tags: bool = True
    display_ids: bool = True
    copy_command: str | None = None

    launcher_settings: Launcher = None
    launcher: InitVar[ Dict | None] = None
    
    display_settings: Display = None
    display: InitVar[ Dict | None] = None


    @staticmethod
    def __add_obj(clazz, obj):
        if obj is None:
            obj = {}

        return clazz(**obj)



    def __post_init__(self, launcher: Dict | None, display: Dict | None):
        self.launcher_settings = self.__add_obj(Launcher, launcher)
        self.display_settings = self.__add_obj(Display, display)



if __name__=="__main__":
    g = General()
    print(g)
