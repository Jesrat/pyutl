# functions to recycle code

r"""
To use, simply 'import pyutils' 

shellExecute can receive a cmd as str or arr example 
    >>> pyutils.shellExecute('date')
    (b'mi\xc3\xa9 ene 30 11:35:00 CST 2019\n', b'')
    >>> pyutils.shellExecute(['echo',"'hola mundo'"])
    (b"'hola mundo'\n", b'')
"""

__author__ = 'Josue Gomez <jgomez@jesrat.com>'
__version__ = '2.0'
__all__ = [ 'resizeTTY', 'shellExecute', 'progressBar', 'getSensible', ]
__status__  = "production"
__date__    = "30 January 2019"

import os, sys, subprocess
from dotenv import load_dotenv 


result = os.environ.get('MYENV')
load_dotenv(result)

def getSensible(key):
    return os.environ.get(key)

def pysyspath():
    print(sys.version)
    for pth in sys.path:
        print(pth)

def resizeTTY(rows, cols):
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=rows, cols=cols))

def shellExecute(cmd,stdin=None):
    rpt = subprocess.Popen(cmd, stdin=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = rpt.communicate()
    return stdout, stderr

def progressBar(progress, total, status=''):
    ttySize = shellExecute(['stty','size'])
    ttySize = ttySize[0].decode().split(' ')
    barLen = round(int(ttySize[1])/100*90)
    fillLen = int(round(barLen * progress / float(total)))
    percent = round(100.0 * progress / float(total), 1)
    bar = '■' * fillLen + '-' * (barLen - fillLen)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percent, '%', status))
    sys.stdout.flush()