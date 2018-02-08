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


class Logger:
    def __init__(self, logfile, stream):
        """
        Implements redirection of console messages to a log file
        """

        self.terminal = stream
        self.log = open(logfile, 'w')
        self.log.write('Logging started...\n')

    def write(self, message):
        """
        Writes message to terminal and to the log
        :param message: (str)   Message to write
        :return:        None
        """

        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        """
        Not implemented yet
        :return: None
        """
        pass
