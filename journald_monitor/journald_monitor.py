from typing import List, Dict
import subprocess as sp

class JournaldMonitor(object):
    from pathlib import Path
    from pyhocon import ConfigTree

    DEFAULT_JOURNALCTL_COMMAND = ['/usr/bin/env', 'journalctl']

    def __init__(self,
        config: ConfigTree,
        journald_command: List[str] = DEFAULT_JOURNALCTL_COMMAND,
        regexList: List[Dict[str, List[str]]] = []):

        self.__journald_command = journald_command
        self.__regexList = regexList
        self.__config = config

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
        import journald_monitor.actions as actions_module

        for line in self.__journald_iterator:
            line = line.decode('utf-8')

            for d in self.__regexList:
                match = re.match(pattern=d.regex, string=line)

                if match is not None:
                    for action in d.actions:
                        for param in action.params:
                            if isinstance(action.params[param], str):
                                for j, val in enumerate(match.groups(), start=1):
                                    action.params[param] = action.params[param].replace('$' + str(j), val)

                        method = getattr(actions_module, action.name)
                        params = action.params.as_plain_ordered_dict()

                        params['line'] = line
                        params['config'] = self.__config

                        method(**params)

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
            config=config,
            journald_command=config.get_list('monitor.journalctl.command', cls.DEFAULT_JOURNALCTL_COMMAND),
            regexList=config.get_list('monitor.match_list', [])
        )