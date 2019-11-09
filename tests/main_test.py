# pylint: disable=missing-docstring
from unittest.mock import Mock, patch

from lswin import get_windows
from lswin._macos_window import Window


def _get_mock_window(name: str, on_screen: bool) -> Mock:
    window = Mock(autospec=Window)
    window.owner_name = f'owner_{name}'
    window.name = name
    window.is_on_screen = on_screen
    return window


class TestMain:
    def test_get_windows_any_name_on_screen(self):
        window_one = _get_mock_window('one', True)
        window_two = _get_mock_window('two', True)
        window_three = _get_mock_window('three', False)
        all_windows = iter([window_one, window_two, window_three])
        on_screen_windows = iter([window_one, window_two])
        off_screen_windows = iter([window_three])

        with patch.object(Window, 'all', return_value=all_windows) as mock_all_windows,\
                patch.object(Window, 'sort', side_effect=lambda windows: windows) as mock_sort:
            windows = get_windows()
            mock_all_windows.assert_called_once()
            mock_sort.assert_called_once()

            assert all(w in windows for w in on_screen_windows)
            assert not any(w in windows for w in off_screen_windows)

    def test_get_windows_one_name_on_screen(self):
        window_one = _get_mock_window('one', True)
        window_two = _get_mock_window('two', True)
        window_three = _get_mock_window('three', False)
        all_windows = iter([window_one, window_two, window_three])

        with patch.object(Window, 'all', return_value=all_windows) as mock_all_windows,\
                patch.object(Window, 'sort', side_effect=lambda windows: windows) as mock_sort:
            windows = get_windows(f'*{window_one.name}*')
            mock_all_windows.assert_called_once()
            mock_sort.assert_called_once()

            assert window_one in windows
            assert not any(w in windows for w in (window_two, window_three))
