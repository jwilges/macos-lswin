#!/usr/bin/env python
'''lswin: list and filter macOS window names and process IDs'''
import sys
from argparse import ArgumentParser
from fnmatch import fnmatch

from ._macos_window import Window

__version__ = '0.1'


def get_windows(name_filter: str = None, include_off_screen: bool = False):
    '''Return all windows optionally filtered by name or on-screen state'''
    def included(window: Window) -> bool:
        if include_off_screen or window.is_on_screen:
            if name_filter:
                name = f'{window.owner_name or ""} {window.name or ""}'.lower()
                return fnmatch(name, name_filter.lower())
            if window.name:
                return len(window.name.strip()) > 0
        return False

    windows = tuple(w for w in Window.all() if included(w))

    return Window.sort(windows)


def main():
    '''The main command-line entry point'''
    parser = ArgumentParser()
    parser.add_argument('--filter', '-f', default=None)
    parser.add_argument('--all', '-a', action='store_true')
    arguments = parser.parse_args()

    windows = get_windows(arguments.filter, arguments.all)
    if windows:
        message = '{0:>6}  {1:>6}  {2:43}  {3:>5}  {4:>5}'
        print(message.format('PID', 'WID', 'Process: Window', 'X', 'Y'))
        print('-'*6, '-'*6, '-'*43, '-'*5, '-'*5, sep='  ')
        for window in windows:
            name = str(window)
            if len(name) > 43:
                name = name[:40] + '...'
            print(message.format(window.owner_pid, window.number, name, window.x, window.y))


if __name__ == '__main__':
    main()
