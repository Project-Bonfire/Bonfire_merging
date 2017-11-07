#!/usr/bin/python3

"""
The main simulation / synthesis script of the Bonfire project

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

import sys
import time
import logging

from Scripts.include.misc import arg_parser
from Scripts.include.misc.Logger import Logger
from Scripts.include.parser.conf_parser import *
from Scripts.include.parser.vhdl_parser import *

try:
    import yaml

except ImportError as e:
    yaml = None
    print_msg(MSG_ERROR, 'Module pyyaml is not installed. Run \'pip3 install pyyaml\' to install it')
    raise ImportError(e)


def main():
    """
    Main function.
    :return:    1 in case of an error, 0 otherwise
    """

    # Argument parsing
    try:
        args = arg_parser.parse()

    except ValueError as err:
        print_msg(MSG_ERROR, str(err))
        return package.FAILURE

    # Check if the temporary folder exists. If it does, clear it, if not, create it.
    try:
        check_dir(package.LOG_DIR, True, args.debug)
        check_dir(package.TRACE_DIR, True, args.debug)

    except (OSError, ValueError) as err:
        print_msg(MSG_ERROR, str(err))
        return package.FAILURE

    # Just for getting a copy of the current console
    sys.stdout = Logger()

    # Setup Logging
    logging.basicConfig(filename=package.LOG_DIR + '/Logging_Log_' + str(time.time()) + '.log', level=logging.DEBUG)
    logging.info('Logging started...')

    config_file, exec_mode = extract_config_path(args)

    try:
        config = read_config(config_file, exec_mode, True, logging)

    except FileNotFoundError as err:
        print_msg(MSG_ERROR, 'Cannot open config file: ' + str(err))
        return package.FAILURE

    except yaml.scanner.ScannerError as err:
        print_msg(MSG_ERROR, 'Syntax error while reading config file: \n' + str(err))
        return package.FAILURE

    except (ValueError, RuntimeError) as err:
        print_msg(MSG_ERROR, str(err))
        return package.FAILURE

    # Parse the VHDL files for building the NW file and the TB
    try:
        parse_vhdl(config, logging)

    except FileNotFoundError as err:
        print_msg(MSG_ERROR, str(err))
        return package.FAILURE

    return package.SUCCESS


if __name__ == '__main__':

    # Test for Python3
    if sys.version_info < (3, 0):
        print_msg(MSG_ERROR, 'This script needs Python version 3 to run!')
        sys.exit(package.FAILURE)

    else:
        return_code = main()
        sys.exit(return_code)
