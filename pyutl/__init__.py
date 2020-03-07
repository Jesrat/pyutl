r"""
To use, simply 'import pyutils' 

shellExecute can receive a cmd as str or arr example 
    >>> pyutils.shell_execute('date')
    (b'mi\xc3\xa9 ene 30 11:35:00 CST 2019\n', b'')
    >>> pyutils.shell_execute(['echo',"'hello world'"])
    (b"'hello world'\n", b'')
"""

__title__ = 'pyutl'
__description__ = 'functions and utilities to recycle code'
__url__ = 'https://github.com/Jesrat/pyutl.git'
__version__ = '2.7'
__author__ = 'Josue Gomez <jgomez@jesrat.com>'
__email__ = "jgomez@binkfe.com"
__maintainer__ = "Josue Gomez"
__license__ = "MIT"
__all__ = ['', ]
__status__ = "production"
__date__ = "30 January 2019"
__copyright__ = 'Copyright 2019 Josue Gomez'


import sys
import subprocess


def resize_tty(rows, cols):
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=rows, cols=cols))


def shell_execute(cmd, stdin=None):
    proc = subprocess.Popen(cmd, stdin=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    return stdout, stderr, proc.returncode


def progress_bar(progress, total, status=''):
    tty_size = shell_execute(['stty', 'size'])
    tty_size = tty_size[0].decode().split(' ')
    bar_len = round(int(tty_size[1])/100*90)
    fill_len = int(round(bar_len * progress / float(total)))
    percent = round(100.0 * progress / float(total), 1)
    bar = '■' * fill_len + '-' * (bar_len - fill_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percent, '%', status))
    sys.stdout.flush()


def read_streamed_file(file, chunk_size=10):
    """
    Reads a hugh file by chunks (10 lines default)
    :param file
    :param chunk_size (10 lines default)
    :return: chunk by chunk
    """
    counter = 0
    ret_lines = []
    with open(file) as f:
        while True:
            counter += 1
            line = f.readline()
            if line:
                ret_lines.append((counter, line))
            if (counter/chunk_size).is_integer() or not line:
                yield ret_lines
                ret_lines = []
            if not line:
                break
