#!/usr/bin/env python
'''lswin: list and filter macOS window names and process IDs'''
import sys
from argparse import ArgumentParser
from fnmatch import fnmatch
from typing import Iterable

from ._macos_window import Window

__version__ = '0.2'


def get_windows(name_filter: str = '', include_off_screen: bool = False) -> Iterable[Window]:
    '''Return all windows optionally filtered by name or on-screen state'''
    name_filter = name_filter.lower()
    def included(window: Window) -> bool:
        if include_off_screen or window.is_on_screen:
            if name_filter:
                return any(fnmatch((name or '').lower(), name_filter)
                           for name in (window.owner_name, window.name))
            return bool(window.owner_name.strip() or window.name.strip())
        return False

    windows = tuple(w for w in Window.all() if included(w))

    return Window.sort(windows)


def print_window_table(windows: Iterable[Window], out_file=sys.stdout):
    '''Print a fixed-width table of window objects'''
    if windows:
        message = '{0:>6}  {1:>6}  {2:43}  {3:>5}  {4:>5}'
        print(message.format('PID', 'WID', 'Process: Window', 'X', 'Y'), file=out_file)
        print('-'*6, '-'*6, '-'*43, '-'*5, '-'*5, sep='  ', file=out_file)
        for window in windows:
            name = str(window)
            if len(name) > 43:
                name = name[:40] + '...'
            print(message.format(window.owner_pid, window.number, name, window.x, window.y), file=out_file)


def main():
    '''The main command-line entry point'''
    parser = ArgumentParser(description=__doc__.partition('\n')[0])
    parser.add_argument('--version', '-v', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument('--filter', '-f', default='',
                        help='filter window names using a case-insensitive POSIX glob-style pattern (e.g. "*term*")')
    parser.add_argument('--all', '-a', action='store_true',
                        help='include both on- and off-screen windows')
    arguments = parser.parse_args()

    windows = get_windows(arguments.filter, arguments.all)
    print_window_table(windows)


if __name__ == '__main__':
    main()
