"""
Includes utility functions for the script

Copyright (C) 2016 - 2017 Karl Janson, Siavoosh Payandeh Azad, Behrad Niazmand

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

import os
import re
from difflib import SequenceMatcher
from Scripts.include.misc import package

# Check_dir return values
CHECK_DIR_ERROR = -1
DIR_EXISTS = 0
DIR_NOT_EXISTS = 1

# Message types
MSG_INFO = 0
MSG_WARN = 1
MSG_ERROR = 2
MSG_BLUE_INFO = 3
MSG_DEBUG = 4


def max_two_char_diff(string1, string2):
    """
    Finds if two string have only up to two character difference
    :param string1: (str) First string for comparison
    :param string2: (str) Second string for comparison
    :return:        True if strings are the same length with
                    only one character difference, False otherwise
    """

    if len(string1) == len(string2):

        match = SequenceMatcher(None, string1, string2).find_longest_match(0, len(string1), 0, len(string2))

        if len(string1) - match.size < 3:
            return True

    return False


def get_output_path(exec_mode, logger):
    """
    Calculates and creates an output directory based on the script's arguments.
    :param exec_mode:   (int) Execution mode
    :param logger:      (Logger) Logger instance
    :return:            Path to the output directory
    """

    if exec_mode == package.EXEC_TYPE_SIMUL:
        output_dir = package.SIMUL_DIR

    elif exec_mode == package.EXEC_TYPE_SYNTH:
        output_dir = package.SYNTH_DIR

    elif exec_mode == package.EXEC_TYPE_FPGA:
        output_dir = package.FPGA_DIR

    else:
        raise ValueError("Unknown output. How did we get here???")

    check_dir(output_dir, True, logger)

    return output_dir


def word_in_string(word, string):
    """
    Find if there is a word in a string.
    :param word:    (str) Word to search for
    :param string:  (str) The string to search the word from
    :return:        _sre.SRE_match object if word is found, None otherwise
    """

    return re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE).search(string)


def colorize_text(bold, underlined, string, color=package.COLOR_END):
    """
    Colorize a string for the terminal
    :param bold:        (bool) Should the text be bold
    :param underlined:   (bool) Should the text be underlined
    :param string:      (str)  The string to be colorized
    :param color:       (str)  Color code for the text (from package)
    :return:            (str)  Colorized string
    """

    bold_str = package.TEXT_TYPE_BOLD if bold else ''
    underlined_str = package.TEXT_TYPE_UNDERLINED if underlined else ''

    return bold_str + underlined_str + color + string + package.COLOR_END


def print_msg(severity, msg):
    """
    Prints a message with a defined severity on the screen
    :param severity:    (int) Message severity (definitions in the beginning of this file)
    :param msg:         (str) Message to be printed
    :return:            None
    """

    if severity == MSG_INFO:
        msg_string = colorize_text(True, False, 'INFO: ') + msg

    elif severity == MSG_WARN:
        msg_string = colorize_text(True, False, 'WARNING: ', package.COLOR_YELLOW) + msg

    elif severity == MSG_ERROR:
        msg_string = colorize_text(True, False, 'ERROR: ', package.COLOR_RED) + msg

    elif severity == MSG_BLUE_INFO:
        msg_string = colorize_text(True, False, 'INFO: ', package.COLOR_BLUE) + msg

    elif severity == MSG_DEBUG:
        msg_string = colorize_text(True, False, 'DEBUG: ') + msg

    else:
        msg_string = msg

    print(msg_string)


def ask_user_input_yn(question):
    """
    Asks user a yes or no question
    :param question:    (string) Question to be asked
    :return:            (bool)   True if used answered 'yes', False if 'no'
    """

    input_ok = False
    user_input = input(question)

    while not input_ok:
        if user_input == 'y' or user_input == 'n':
            input_ok = True

        else:
            user_input = input('Invalid input. y/n: ')

    return user_input == 'y'


def check_dir(dir_path, create_dir, logger):
    """
    Check if directory exists. If not, it will be created.
    :param dir_path:     (str)   Path to the directory
    :param create_dir:   (bool)  Should the directory be created in case it does not exist
    :param logger:       (Logger)  Instance to system logger
    :return:             (int)   -1 In case of an error, a positive value otherwise
    """

    # Check for the existence of the sources directory
    if os.path.exists(dir_path):

        # Path exists, but is not a file
        if not os.path.isdir(dir_path):
            print_msg(MSG_WARN, 'File \'' + dir_path +
                      '\' already exists, but it is not a directory.\n'
                      'To continue, you will need to remove it.')

            user_input = ask_user_input_yn('Do you want to remove it now? y/n\n')

            # Remove the existing file
            if user_input:  # User said 'yes'
                logger.info(dir_path + ': Removing existing file...')

                os.remove(dir_path)

            else:  # User said 'no'
                raise ValueError('Operation was cancelled by user')

            # Create a directory in place of the file
            if create_dir:
                logger.info(dir_path + ': Creating the directory')

                os.makedirs(dir_path)

                return DIR_EXISTS

            else:
                return DIR_NOT_EXISTS

        # Directory already exists
        else:
            logger.info(dir_path + ': Using existing directory')
            return DIR_EXISTS

    else:
        if create_dir:
            logger.info('Directory ' + dir_path + 'not found. Creating it.')

            os.makedirs(dir_path)

            return DIR_EXISTS

        else:
            return DIR_NOT_EXISTS
