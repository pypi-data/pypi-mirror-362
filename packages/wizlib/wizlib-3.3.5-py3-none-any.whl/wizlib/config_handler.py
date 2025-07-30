from argparse import Namespace
from pathlib import Path
import os
from dataclasses import dataclass
import re
import shlex
import subprocess
from unittest.mock import patch

from yaml import load
from yaml import Loader
from wizlib.handler import Handler

from wizlib.error import ConfigHandlerError
from wizlib.parser import WizParser


class ConfigHandler(Handler):
    """
    Handle app-level configuration, where settings could come from specific
    settings (such as from argparse), environment variables, or a YAML file.
    Within the Python code, config keys are underscore-separated all-lower.

    A ConfigHandler returns null in the case of a missing value, assuming that
    commands can handle their own null cases.
    """

    name = 'config'

    def __init__(self, file=None, yaml=None):
        self.file = file
        self.yaml_dict = yaml
        self.cache = {}

    @property
    def yaml(self):
        if hasattr(self, '_yaml'):
            return self._yaml

        # If yaml_dict was provided, use it directly
        if self.yaml_dict is not None:
            self._yaml = self.yaml_dict
            return self._yaml

        path = None
        if self.file:
            path = Path(self.file)
        elif self.app and self.app.name:
            localpath = Path.cwd() / f".{self.app.name}.yml"
            homepath = Path.home() / f".{self.app.name}.yml"
            if (envvar := self.env(self.app.name + '-config')):
                path = Path(envvar)
            elif (localpath.is_file()):
                path = localpath
            elif (homepath.is_file()):
                path = homepath
        if path:
            with open(path) as file:
                self._yaml = load(file, Loader=Loader)
                return self._yaml

    @staticmethod
    def env(name):
        if (envvar := name.upper().replace('-', '_')) in os.environ:
            return os.environ[envvar]

    def get(self, key: str):
        """Return the value for the requested config entry"""

        # If we already found the value, return it
        if key in self.cache:
            return self.cache[key]

        # Environment variables take precedence
        if (result := self.env(key)):
            self.cache[key] = result
            return result

        # Otherwise look at the YAML
        if (yaml := self.yaml):
            split = key.split('-')
            while (val := split.pop(0)) and (val in yaml):
                yaml = yaml[val] if val in yaml else None
                if not split:
                    result = evaluate_yaml_value(yaml)
                    self.cache[key] = result
                    return result

    @classmethod
    def fake(cls, **vals):
        """Return a fake ConfigHandler with forced values, for testing"""
        self = cls()
        self.cache = {k.replace('_', '-'): vals[k] for k in vals}
        return self


def os_process(match):
    """Run a subprocess"""
    command_string = match.group(1).strip()
    command = shlex.split(command_string)
    result = subprocess.run(command, capture_output=True)
    return result.stdout.decode().strip()


def evaluate_yaml_value(yaml: str) -> str:
    """When getting a value from YAML, evaluate shell commands"""
    text = yaml.strip()
    return re.sub(r'\$\((.*?)\)', os_process, text)
