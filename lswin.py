#!/usr/bin/env python
'''lswin: list and filter macOS window names and process IDs'''
__version__ = '1.0.0'


class Window(object):
    def __init__(self, window):
        self.is_on_screen = window.get('kCGWindowIsOnscreen', False)
        self.number = window.get('kCGWindowNumber')
        self.name = window.get('kCGWindowName')
        self.owner_pid = window.get('kCGWindowOwnerPID')
        self.owner_name = window.get('kCGWindowOwnerName')

        bounds = window.get('kCGWindowBounds', {})
        self.x = int(bounds.get('X', 0))
        self.y = int(bounds.get('Y', 0))
        self.width = int(bounds.get('Width', 0))
        self.height = int(bounds.get('Height', 0))


    def __str__(self):
        owner = self.owner_name or f'<{self.owner_pid}>'
        name = self.name or f'<{self.number}>'
        return f'{owner}: {name}'


    def __repr__(self):
        return f'<Window: PID: {self.owner_pid}; "{str(self)}">'


def getWindows(filter: str=None, all: bool=False):
    from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionAll, kCGNullWindowID
    windows = (Window(w) for w in CGWindowListCopyWindowInfo(kCGWindowListOptionAll, kCGNullWindowID))

    def included(window: Window) -> bool:
        from fnmatch import fnmatch
        if all or window.is_on_screen:
            if filter:
                name = f'{window.owner_name or ""} {window.name or ""}'.lower()
                return fnmatch(name, filter.lower())
            elif window.name:
                return len(window.name.strip()) > 0
        return False

    windows = tuple(w for w in windows if included(w))

    return sorted(windows, key=lambda w: (w.owner_pid, w.number))


if __name__ == "__main__":
    import sys
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('--filter', '-f', default=None)
    parser.add_argument('--all', '-a', action='store_true')
    arguments = parser.parse_args()

    windows = getWindows(arguments.filter, arguments.all)
    if windows:
        message = '{0:>6}  {1:>6}  {2:43}  {3:>5}  {4:>5}' 
        print(message.format('PID', 'WID', 'Process: Window', 'X', 'Y'))
        print('-'*6, '-'*6, '-'*43, '-'*5, '-'*5, sep='  ')
        for w in windows:
            name = str(w)
            if len(name) > 43:
                name = name[:40] + '...'
            print(message.format(w.owner_pid, w.number, name, w.x, w.y))