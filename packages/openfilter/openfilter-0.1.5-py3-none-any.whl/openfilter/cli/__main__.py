import sys

from .common import SCRIPT
from .cmd_info import cmd_info
from .cmd_run import cmd_run


def main():
    args = sys.argv[2:]
    cmd  = sys.argv[1] if len(sys.argv) > 1 else ''

    if cmd_func := getattr(sys.modules[__name__], f'cmd_{cmd}', None):
        cmd_func(args)

    else:
        print(f"""
usage: {SCRIPT} COMMAND ...

Commands:
  run       Directly run one or more filter(s)
  logs      Show filter(s) logs
  info      Get help on a specific filter

Run '{SCRIPT} COMMAND --help' for more information on a command.
""".strip())


if __name__ == '__main__':
    main()
