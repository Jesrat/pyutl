# functions to recycle code

r"""
To use, simply 'import pyutils' 

shellExecute can receive a cmd as str or arr example 
    >>> pyutils.shell_execute('date')
    (b'mi\xc3\xa9 ene 30 11:35:00 CST 2019\n', b'')
    >>> pyutils.shell_execute(['echo',"'hello world'"])
    (b"'hello world'\n", b'')
"""

__author__ = 'Josue Gomez <jgomez@jesrat.com>'
__maintainer__ = "Josue Gomez"
__email__ = "jgomez@binkfe.com"
__license__ = "MIT"
__version__ = '2.0'
__all__ = ['', ]
__status__ = "production"
__date__ = "30 January 2019"


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
