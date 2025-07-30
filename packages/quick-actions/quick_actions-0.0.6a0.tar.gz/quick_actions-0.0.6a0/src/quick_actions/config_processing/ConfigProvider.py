import tomllib
from pathlib import Path
from typing import List, Dict
from benedict import benedict
import os
import sys

from quick_actions.config_processing.config_classes.Action import Action
from quick_actions.config_processing.config_classes.General import General
from quick_actions.config_processing.ActionProcessor import ActionProcessor
from quick_actions import constants

class ConfigProvider:
    instance = None

    @classmethod
    def get_instance(cls, config_path: Path = None):
        if cls.instance is None:
            if config_path is None:
                print("INTERNAL ERROR: this should not happen :(", file=sys.stderr)
            cls.instance = cls(config_path)
        return cls.instance


    def __init__(self, config_path: Path):
        self.config_path = config_path

        self.collect()

    @property
    def actions(self):
        return self.settings["actions"]

    @property
    def action_prefixes(self):
        return ActionProcessor.get_prefixes(self.settings["actions"])

    @property
    def actions_by_label(self):
        return { x.label: x for key, x in self.actions.items()}


    def folder_generator(self):
        return self.config_path.rglob('*.toml')


    def collect_toml(self):
        settings = benedict(keypath_separator=None)
        for path in self.folder_generator():
            relative_dirs = path.parent.relative_to(self.config_path).parts

            with open(path, "rb") as f:
                new_values = tomllib.load(f)

                ActionProcessor.expand_file_paths(path.parent, new_values)


                for part in reversed(relative_dirs):
                    new_values = { part: new_values }

                settings.merge(new_values)
            
        return settings


    def collect(self):
        settings = self.collect_toml()

        if settings.get("actions") is None:
            # TODO: rethink this
            settings["actions"] = {
                "noID.errorMessage.initial_warning": {
                    "label": "Please define some actions!"
                }
            }
            print("Please define some actions!", file=sys.stderr)

        if settings.get("general") is None:
            settings["general"] = {}

        self.settings = {
            "general": General(**settings["general"])
        }

        self.settings["actions"], self.envs = ActionProcessor.flat_actions(settings["actions"])

    @property
    def general(self):
        return self.settings["general"]


    @staticmethod
    def get_default_config_path():
        home = Path.home()

        if os.name == 'posix':  # Unix-like systems (Linux, macOS, etc.)
            config_path = home / '.config' / constants.APP_NAME
        elif os.name == 'nt':  # Windows
            config_path = home / 'AppData' / 'Local' / constants.APP_NAME
        else:
            print("WARNING: Unsupported operating system, you may use -C option", file=sys.stderr)
            config_path = home

        return config_path
