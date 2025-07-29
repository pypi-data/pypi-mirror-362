"""
Logging module for cx-Freeze.
"""

__all__ = ['getLogger', 'INFO', 'WARN', 'DEBUG', 'TRACE', 'ERROR', 'FATAL']

import logging
import sys
import time
from logging import DEBUG, ERROR, FATAL, INFO, WARN, getLogger

TRACE = logging.TRACE = DEBUG - 5
logging.addLevelName(TRACE, 'TRACE')

FORMAT = '%(relativeCreated)d %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = getLogger('cx_Freeze')


def __add_options(parser):
    levels = ('TRACE', 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')
    parser.add_argument(
        '--log-level',
        choices=levels,
        metavar="LEVEL",
        default='INFO',
        dest='loglevel',
        help='Amount of detail in build-time console messages. LEVEL may be one of %s (default: %%(default)s).' %
        ', '.join(levels),
    )


def __process_options(parser, opts):
    try:
        level = getattr(logging, opts.loglevel.upper())
    except AttributeError:
        parser.error('Unknown log level `%s`' % opts.loglevel)
    else:
        logger.setLevel(level)

class Logger(object):
    def __init__(self, loggerName):
        self.name = loggerName
        self.logger = getLogger(loggerName)
        self.alive = True
        self.timer = time.time()
        self.buffer = ''
        self.stdout = sys.stdout
        sys.stdout = self

    def __enter__(self):
        self.timer = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        if self.alive:
            sys.stdout = self.stdout
            self.alive = False

    def write(self,message):
        timer = time.time()
        if timer - self.timer >= 1:
            self.logger.info(self.buffer + message)
            self.timer = timer
            self.buffer = ''
        else:
            self.buffer = self.buffer + message
        self.stdout.write(message)

    def flush(self):
        pass