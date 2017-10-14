"""
Implements redirection of console messages to a log file
Copyright (C) 2016 - 2017 Karl Janson, Siavoosh Payandeh Azad, Behrad Niazmand

Release under the GPLv3 license:
https://www.gnu.org/licenses/gpl-3.0.en.html
"""

import sys
import time

from Scripts.include.misc.package import LOG_DIR


class Logger(object):
    def __init__(self):
        """
        Implements redirection of console messages to a log file
        """

        self.terminal = sys.stdout
        self.log = open(LOG_DIR + '/Console_log_' + str(time.time()) + '.log', 'a')

    def write(self, message):
        """
        Writes message to terminal and to the log
        :param message: (str)   Message to write
        :return:        None
        """

        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass
