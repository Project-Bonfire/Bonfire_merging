"""
Implements redirection of console messages to a log file
Copyright (C) 2016 - 2018 Karl Janson, Siavoosh Payandeh Azad, Behrad Niazmand

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import logging
import pprint

from Scripts.include.misc.package import *
from Scripts.include.misc.Logger import Logger
from Scripts.include.misc.helper_func import colorize_text


class ScreenLogger(Logger):
    def __init__(self, debug, console_log, logfile):
        """
        Implements redirection of console messages to a log file
        :param debug:   (bool)  Specifies if we are in debug mode
        """

        super().__init__(console_log, sys.__stdout__)

        self.debug_flag = debug
        # Set up generic logging
        log_level = logging.DEBUG if debug else logging.INFO

        logging.basicConfig(filename=logfile, level=log_level)

        self.debug('Logging started...')

    def formatDict(self, dictionary):
        """
        Return a nicely formatted version of dictionary
        """
        return pprint.pformat(dictionary)  + '\n'

    def info(self, msg, console=True):
        """
        Logs an info message
        :param msg:     (str)   message to be logged
        :param console  (bool)  If true, the message will also be displayed on console
        :return:
        """
        logging.info(msg)
        if console:
            self.write(colorize_text(True, False, 'INFO: ') + msg + '\n')

    def warning(self, msg, console=True):
        """
        Logs an info message
        :param msg:     (str)   message to be logged
        :param console  (bool)  If true, the message will also be displayed on console
        :return:
        """
        logging.warning(msg)
        if console:
            self.write(colorize_text(True, False, 'WARNING: ', COLOR_YELLOW) + msg + '\n')

    def error(self, msg, console=True):
        """
        Logs an info message
        :param msg:     (str)   message to be logged
        :param console  (bool)  If true, the message will also be displayed on console
        :return:
        """
        logging.error(msg)
        if console:
            self.write(colorize_text(True, False, 'ERROR: ', COLOR_RED) + msg + '\n')

    def debug(self, msg, console=True):
        """
        Logs an info message
        :param msg:     (str)   message to be logged
        :param console  (bool)  If true, the message will also be displayed on console
        :return:
        """
        logging.debug(msg)
        if console and self.debug_flag:
            self.write(colorize_text(True, False, 'DEBUG: ') + msg + '\n')

    def blue_info(self, msg, console=True):
        """
        Logs an info message
        :param msg:     (str)   message to be logged
        :param console  (bool)  If true, the message will also be displayed on console
        :return:
        """
        logging.info(msg)
        if console:
            self.write(colorize_text(True, False, 'INFO: ', COLOR_BLUE) + msg + '\n')
