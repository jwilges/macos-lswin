# pylint: disable=missing-docstring,no-self-use
import argparse
import sys
from unittest.mock import MagicMock, Mock, patch
import pytest

import lswin
from lswin._macos_window import Window


def _get_mock_window(name: str, on_screen: bool) -> Mock:
    window = MagicMock(autospec=Window)
    window.owner_pid = 1
    window.number = 11
    window.x = 10
    window.y = 20
    window.owner_name = f'owner_{name}'
    window.name = name
    window.is_on_screen = on_screen
    window.__str__ = lambda self: f'{self.owner_name} {self.name}'
    return window


class TestMain:
    def test_get_windows_any_name_on_screen(self):
        window_one = _get_mock_window('one', on_screen=True)
        window_two = _get_mock_window('two', on_screen=True)
        window_three = _get_mock_window('three', on_screen=False)
        all_windows = iter([window_one, window_two, window_three])
        on_screen_windows = iter([window_one, window_two])
        off_screen_windows = iter([window_three])

        with patch.object(Window, 'all', return_value=all_windows) as mock_all_windows,\
                patch.object(Window, 'sort', side_effect=lambda windows: windows) as mock_sort:
            windows = lswin.get_windows()
            mock_all_windows.assert_called_once()
            mock_sort.assert_called_once()

            assert all(w in windows for w in on_screen_windows)
            assert not any(w in windows for w in off_screen_windows)

    def test_get_windows_one_name_on_screen(self):
        window_one = _get_mock_window('one', on_screen=True)
        window_two = _get_mock_window('two', on_screen=True)
        window_three = _get_mock_window('three', on_screen=False)
        all_windows = iter([window_one, window_two, window_three])

        with patch.object(Window, 'all', return_value=all_windows) as mock_all_windows,\
                patch.object(Window, 'sort', side_effect=lambda windows: windows) as mock_sort:
            windows = lswin.get_windows(f'*{window_one.name}*')
            mock_all_windows.assert_called_once()
            mock_sort.assert_called_once()

            assert window_one in windows
            assert not any(w in windows for w in (window_two, window_three))

    def test_main_get_windows_arguments(self):
        mock_arguments = Mock()
        mock_arguments.filter = Mock()
        mock_arguments.all = Mock()
        mock_windows = Mock()
        with patch.object(argparse.ArgumentParser, 'parse_args', return_value=mock_arguments) as mock_parse_args,\
                patch.object(lswin, 'get_windows', return_value=mock_windows) as mock_get_windows,\
                patch.object(lswin, 'print_window_table') as mock_print_window_table:
            lswin.main()

            # Verify get_windows() executes with --filter and --all CLI argument values
            mock_parse_args.assert_called_once()
            mock_get_windows.assert_called_once_with(mock_arguments.filter, mock_arguments.all)

            # Verify print_windows() executes with the result of get_windows()
            mock_print_window_table.assert_called_once_with(mock_windows)

    @pytest.mark.parametrize(
        ('out_file',),
        [(sys.stdout,), (sys.stderr,)],
        ids=['stdout', 'stderr'])
    def test_main_print_window_table_arguments(self, out_file):
        window_one = _get_mock_window('one', on_screen=True)
        window_two = _get_mock_window('two', on_screen=True)
        with patch('builtins.print') as mock_print:
            lswin.print_window_table((window_one, window_two), out_file=out_file)

            # Verify print() executes at least with expected window names
            mock_print.assert_called()
            expected_window_names = [str(window_one), str(window_two),]
            for output in mock_print.call_args_list:
                if not expected_window_names:
                    break
                if expected_window_names[0] in ''.join(output[0]):
                    expected_window_names.pop(0)
                    assert output[-1]['file'] == out_file
            assert not expected_window_names, f'{len(expected_window_names)} windows were not found'
