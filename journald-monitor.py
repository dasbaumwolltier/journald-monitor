import logging.config

import logging as log

from argparse import ArgumentParser
from pathlib import Path

from journald_monitor import JournaldMonitor

def main():
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

if __name__ == '__main__':
    main()