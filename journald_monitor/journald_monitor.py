import logging as log

from .utils import call_function, get_from_dict

def main():
    import logging.config

    from argparse import ArgumentParser
    from pathlib import Path

    parser = ArgumentParser("journald-monitor")

    parser.add_argument('-c', '--config', metavar='CONFIG', type=str, required=True,
        help='The config file used to configure this program')
    parser.add_argument('-l', '--log-config', metavar='LOGCONFIG', default=None, type=str, required=False,
        help='A config file in the python logging config format')

    args = parser.parse_args()

    if args.log_config is None:
        log.basicConfig(
            level=log.DEBUG
        )
    else:
        log.config.fileConfig(args.logconfig)

    with JournaldMonitor.create(args.config) as monitor:
        monitor.process_logs()

class JournaldMonitor(object):
    from pathlib import Path
    from typing import List, Dict

    DEFAULT_JOURNALCTL_COMMAND = ['/usr/bin/env', 'journalctl']

    def __init__(self,
        config: Dict[str, dict],
        journald_command: List[str] = DEFAULT_JOURNALCTL_COMMAND
    ):

        self.__config = config
        self.__journald_command = journald_command

        self.__rules = get_from_dict(config, 'rules', {})

    @classmethod
    def create(cls, config_file: Path) -> 'JournaldMonitor':
        return cls.__parse_config(config_file)

    def attach_to_journald(self):
        import subprocess as sp

        command = self.__journald_command + ['-f']

        self.__journald_process = sp.Popen(command, stdout=sp.PIPE)
        self.__journald_iterator = iter(self.__journald_process.stdout.readline, b'')

    def detach_from_journald(self):
        self.__journald_process.terminate()

    def process_logs(self):
        import re

        import journald_monitor.actions as actions_module
        import journald_monitor.triggers as triggers_module

        for line in self.__journald_iterator:
            line = line.decode('utf-8')

            for name, rule in self.__rules.items():
                for trigger_object in get_from_dict(rule, 'triggers', {}):
                    trigger_name = next(iter(trigger_object.keys()))
                    trigger_function = getattr(triggers_module, trigger_name, None)

                    if trigger_function is None:
                        log.error('Could not find trigger {}!', trigger_function)
                        continue

                    trigger_params: dict = trigger_object[trigger_name]

                    try:
                        trigger_result = None
                        if isinstance(trigger_params, str):
                            trigger_result = trigger_function(line, self.__config, trigger_params)
                        elif isinstance(trigger_params, list):
                            trigger_result = trigger_function(line, self.__config, *trigger_params)
                        elif isinstance(trigger_params, dict):
                            trigger_params['line'] = line
                            trigger_params['config'] = self.__config

                            trigger_result = trigger_function(**trigger_params)
                    except KeyboardInterrupt as e:
                        raise
                    except:
                        log.exception('Exception occurred in execution of trigger!')
                        continue

                    if trigger_result is None:
                        continue

                    log.debug('Matched line "%s" with trigger "%s"', line.strip(), trigger_name)

                    for action in rule['actions']:
                        action_name = action['name']
                        action_params = action['params']

                        action_params['line'] = line
                        action_params['config_dict'] = self.__config['configs']

                        action_function = getattr(actions_module, action_name, None)
                        execute_action_function = getattr(triggers_module, trigger_name + '_execute_action', None)

                        if action_function is None or execute_action_function is None:
                            continue

                        try:
                            execute_action_function(trigger_result, action_params, action_function)
                        except KeyboardInterrupt as e:
                            raise
                        except:
                            log.exception('Exception occured in execution of action!')

                    break

    def __enter__(self):
        self.attach_to_journald()
        return self

    def __exit__(self, type, value, traceback):
        self.detach_from_journald()

    @classmethod
    def __parse_config(cls, config_file: Path):
        import yaml

        config = {}
        with open(config_file) as f:
            config = yaml.load(f.read(), Loader=yaml.FullLoader)

        return JournaldMonitor(
            config=config,
            journald_command=get_from_dict(config, 'monitor.journalctl.command', cls.DEFAULT_JOURNALCTL_COMMAND)
        )
