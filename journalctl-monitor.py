from argparse import ArgumentParser
from pathlib import Path

from journalctl_monitor import JournalctlMonitor

def main():
    parser = ArgumentParser("journalctl-monitor")

    parser.add_argument('-c', '--config', metavar='CONFIG', type=str, required=True,
        help="The config file used to configure this program")

    args = parser.parse_args()

    journalctl_monitor = JournalctlMonitor(Path(args.config))
    journalctl_monitor.attach_to_journalctl()

if __name__ == '__main__':
    main()