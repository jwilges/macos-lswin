# pylint: disable=missing-docstring,no-self-use
from lswin._macos_window import Window


class TestMacosWindow:
    def test_window_attributes(self):
        macos_api_window = {
            'kCGWindowIsOnscreen': True,
            'kCGWindowNumber': 1,
            'kCGWindowName': 'window_name',
            'kCGWindowOwnerPID': 2,
            'kCGWindowOwnerName': 'owner_name',
            'kCGWindowBounds': {
                'X': 3,
                'Y': 4,
                'Width': 5,
                'Height': 6
            },
            'kCGWindowMemoryUsage': 7,
        }
        window = Window(macos_api_window)
        assert window.is_on_screen
        assert window.number == 1
        assert window.name == 'window_name'
        assert window.owner_pid == 2
        assert window.owner_name == 'owner_name'
        assert window.x == 3
        assert window.y == 4
        assert window.width == 5
        assert window.height == 6
        assert window.memory_bytes == 7

    def test_window_default_attributes(self):
        macos_api_window = {
            'kCGWindowNumber': 1,
            'kCGWindowName': 'window_name',
            'kCGWindowOwnerPID': 2,
            'kCGWindowOwnerName': 'owner_name',
            'kCGWindowMemoryUsage': 7,
        }
        window = Window(macos_api_window)
        assert not window.is_on_screen
        assert window.number == 1
        assert window.name == 'window_name'
        assert window.owner_pid == 2
        assert window.owner_name == 'owner_name'
        assert window.x == 0
        assert window.y == 0
        assert window.width == 0
        assert window.height == 0
        assert window.memory_bytes == 7
