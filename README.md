# macos-lswin
*lswin: a commandline utility to list and filter macOS process and window names.*

## Background
This utility provides filtering for windows based on parent process name, window name, and whether or not the process is on the screen.

A similar project, [mac_list_windows_pids](https://github.com/sjitech/mac_list_windows_pids), revealed how straightforward the necessary Quartz core graphics lookups are; so, I reviewed Apple's developer documentation for [`CGWindowListCopyWindowInfo`](https://developer.apple.com/documentation/coregraphics/1455137-cgwindowlistcopywindowinfo) and set out to add primitive UNIX shell style wildcard filtering for process and window names with a simple command line interface.

## Supported Platforms
This utility has been tested on macOS Mojave 10.14.2.

## Usage
### Development Environment
Initialize a development environment using:

```bash
python -m venv --prompt lswin .venv
source .venv/bin/activate
```

### Examples
List all windows with process names or window names beginning with "term":

	$ ./lswin.py -a -f "term*"
       PID     WID  Process: Window                                  X      Y
    ------  ------  -------------------------------------------  -----  -----
      4953    4805  Terminal: <4805>                                 0      0
      4953    4806  Terminal: <4806>                                 0      0
      4953    4813  Terminal: Focus Proxy                          100    100
      4953    7208  Terminal: <7208>                               628     95
      4953    7268  Terminal: Colors                                 0    612
      4953    7269  Terminal: <7269>                               951    433
      4953    8639  Terminal: <8639>                             -1920      0
      4953    8657  Terminal: <8657>                                 0      0
      4953   13111  Terminal: <13111>                              318     68
      4953   13984  Terminal: <13984>                               80      0
      4953   14588  Terminal: Terminal — -bash — 129×22            395    201
      4953   14890  Terminal: Terminal — lswin.py -a -f term...    395    201

List onscreen windows with process names or window names beginning with "term":

    $ ./lswin.py -f "term*"
       PID     WID  Process: Window                                  X      Y
    ------  ------  -------------------------------------------  -----  -----
      4953   14588  Terminal: Terminal — -bash — 129×25            173    496
      4953   14890  Terminal: Terminal — lswin.py -f term* —...    395    201