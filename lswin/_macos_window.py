'''Window-related macOS system calls'''
from __future__ import annotations
from typing import Iterable

class Window:
    '''A high level Window model object to wrap the underlying macOS model and related system calls'''
    def __init__(self, window: dict):
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

        self.memory_bytes = int(window.get('kCGWindowMemoryUsage'))

    def __str__(self):
        owner = self.owner_name or f'<{self.owner_pid}>'
        name = self.name or f'<{self.number}>'
        return f'{owner}: {name}'

    def __repr__(self):
        return f'<Window: PID: {self.owner_pid}; "{str(self)}">'

    @classmethod
    def all(cls) -> Iterable[Window]:
        '''Iterate all windows'''
        try:
            # pylint: disable=no-name-in-module,import-outside-toplevel
            from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionAll, kCGNullWindowID
        except ModuleNotFoundError:
            return
        for window in CGWindowListCopyWindowInfo(kCGWindowListOptionAll, kCGNullWindowID):
            yield cls(window)

    @classmethod
    def sort(cls, windows: Iterable[Window]) -> Iterable[Window]:
        '''Return windows sorted by `owner_pid`, `number` ascending'''
        return sorted(windows, key=lambda w: (w.owner_pid, w.number))
