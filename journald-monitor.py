from argparse import ArgumentParser
from pathlib import Path

from journald_monitor import JournaldMonitor

def main():
    parser = ArgumentParser("journald-monitor")

    parser.add_argument('-c', '--config', metavar='CONFIG', type=str, required=True,
        help="The config file used to configure this program")

    args = parser.parse_args()

    with JournaldMonitor.create(args.config) as monitor:
        monitor.process_logs()

if __name__ == '__main__':
    main()