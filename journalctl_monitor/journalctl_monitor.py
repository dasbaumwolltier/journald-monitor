from typing import List


class JournalctlMonitor(object):
    from pathlib import Path

    def __init__(self, config_file: Path):
        self.__parse_config(config_file)

    def attach_to_journalctl(self):
        ...

    def detach_from_journalctl(self):
        ...

    def __enter__(self):
        self.attach_to_journalctl()
        return self

    def __exit__(self, type, value, traceback):
        self.detach_from_journalctl()

    def __parse_config(self, config_file: Path):
        from pyhocon import ConfigFactory, ConfigTree

        config: ConfigTree = ConfigFactory.parse_file(config_file)

        self.__journalctl_command = config.get_list('journalctl.command', ['/usr/bin/env', 'journalctl'])