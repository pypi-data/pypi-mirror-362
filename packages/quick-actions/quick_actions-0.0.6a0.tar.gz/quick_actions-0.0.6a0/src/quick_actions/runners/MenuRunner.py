from typing import Dict

from quick_actions.config_processing.config_classes.Action import Action
from quick_actions.runners.CommandRunner import CommandRunner
from quick_actions.config_processing.ConfigProvider import ConfigProvider


class MenuRunner:
    def __init__(self, menu_str: str, prompt: str, options_command: str | None = None):
        self.config_provider = ConfigProvider.get_instance()

        if options_command:
            menu_command = f"{options_command} | {self.expand_launcher_command(prompt)}"
        else:
            menu_command = f"echo '{menu_str}' | {self.expand_launcher_command(prompt)}"

        menu_runner = CommandRunner(menu_command, print_err=False)

        if menu_runner.returncode != 0:
            print("User cancelled the operation.")
            exit(0)

        self.menu_output = menu_runner.output.strip()

    def expand_launcher_command(self, prompt: str):
        template = self.config_provider.general.launcher_settings.launcher_command
        template = template.replace("{prompt}", prompt)

        return template
