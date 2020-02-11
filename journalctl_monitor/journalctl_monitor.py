from typing import List, Dict
import subprocess as sp


class JournalctlMonitor(object):
    from pathlib import Path

    DEFAULT_JOURNALCTL_COMMAND = ['/usr/bin/env', 'journalctl']

    def __init__(self,
        journalctl_command: List[str] = DEFAULT_JOURNALCTL_COMMAND,
        regexList: Dict[str, List[str]] = []):

        self.__journalctl_command = journalctl_command
        self.__regexList = regexList

    @classmethod
    def create(cls, config_file: Path) -> 'JournalctlMonitor':
        return cls.__parse_config(config_file)

    def attach_to_journalctl(self):
        command = self.__journalctl_command + ['-f']

        self.__journalctl_process = sp.Popen(command, stdout=sp.PIPE)
        self.__journalctl_iterator = iter(self.__journalctl_process.stdout.readline, b'')

    def detach_from_journalctl(self):
        self.__journalctl_process.terminate()

    def process_logs(self):
        import re
        import journalctl_monitor.actions as actions

        for line in self.__journalctl_iterator:
            for regex, action in self.__regexList.items():
                match = re.match(pattern=regex, string=line)

                if match is not None:
                    for i, param in enumerate(action.params):
                        if isinstance(param, str):
                            for j, val in enumerate(match.groups):
                                action.params[i] = param.replace('$' + j, val)

                    method = getattr(actions, action.name)
                    method({ 'line': line } + action.params)

    def __enter__(self):
        self.attach_to_journalctl()
        return self

    def __exit__(self, type, value, traceback):
        self.detach_from_journalctl()

    @classmethod
    def __parse_config(cls, config_file: Path):
        from pyhocon import ConfigFactory, ConfigTree

        config: ConfigTree = ConfigFactory.parse_file(config_file)

        return JournalctlMonitor(
            journalctl_command=config.get_list('journalctl.command', cls.DEFAULT_JOURNALCTL_COMMAND),
            regexList=config.get_list('monitor.list', [])
        )