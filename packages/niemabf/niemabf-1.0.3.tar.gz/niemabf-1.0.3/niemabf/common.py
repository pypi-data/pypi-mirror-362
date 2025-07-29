# standard imports
from gzip import open as gopen

# non-standard imports
from numpy import uint8

# useful constants
NIEMABF_VERSION = '1.0.3'
DEFAULT_BUFSIZE = 1048576 # 1 MB #8192 # 8 KB

def open_file(fn, mode='rt', buffering=DEFAULT_BUFSIZE):
    '''Open a file (or stream) and return the file(-like) object
    
    Args:
        fn (str): Filename to open, or `-` for standard input (if read mode) or standard output (if write mode)
        mode (str): Mode string containing `r` (read) or `w` (write), and containing `t` (text) or `b` (binary)
        buffering (int): The buffer size when opening a file

    Returns:
        file: The file(-like) object
    '''
    mode = mode.lower().strip()
    if fn == '-':
        if 'w' in mode:
            from sys import stdout as out_file
        else:
            from sys import stdin as out_file
    elif fn.strip().lower().endswith('.gz'):
        out_file = gopen(fn, mode=mode)
    else:
        out_file = open(fn, mode=mode, buffering=buffering)
    return out_file
