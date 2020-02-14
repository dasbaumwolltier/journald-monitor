from typing import List, Dict
import subprocess as sp


class JournaldMonitor(object):
    from pathlib import Path

    DEFAULT_JOURNALCTL_COMMAND = ['/usr/bin/env', 'journald']

    def __init__(self,
        journald_command: List[str] = DEFAULT_JOURNALCTL_COMMAND,
        regexList: Dict[str, List[str]] = []):

        self.__journald_command = journald_command
        self.__regexList = regexList

    @classmethod
    def create(cls, config_file: Path) -> 'JournaldMonitor':
        return cls.__parse_config(config_file)

    def attach_to_journald(self):
        command = self.__journald_command + ['-f']

        self.__journald_process = sp.Popen(command, stdout=sp.PIPE)
        self.__journald_iterator = iter(self.__journald_process.stdout.readline, b'')

    def detach_from_journald(self):
        self.__journald_process.terminate()

    def process_logs(self):
        import re
        import journald_monitor.actions as actions

        for line in self.__journald_iterator:
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
        self.attach_to_journald()
        return self

    def __exit__(self, type, value, traceback):
        self.detach_from_journald()

    @classmethod
    def __parse_config(cls, config_file: Path):
        from pyhocon import ConfigFactory, ConfigTree

        config: ConfigTree = ConfigFactory.parse_file(config_file)

        return JournaldMonitor(
            journald_command=config.get_list('journald.command', cls.DEFAULT_JOURNALCTL_COMMAND),
            regexList=config.get_list('monitor.list', [])
        )