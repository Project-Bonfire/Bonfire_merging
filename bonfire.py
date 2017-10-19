#!/usr/bin/python3

"""
The main simulation / synthesis script for the Bonfire project

Copyright (C) 2016 - 2017 Karl Janson, Siavoosh Payandeh Azad, Behrad Niazmand

Release under the GPLv3 license:
https://www.gnu.org/licenses/gpl-3.0.en.html
"""

import sys
import logging
import time

from Scripts.include.misc.helper_func import *
from Scripts.include.misc.Logger import Logger
from Scripts.include.misc import package
from Scripts.include.misc import arg_parser
from Scripts.include.misc.process_conf import *

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

    config_file = extract_config_path(args)

    try:
        config = read_config(config_file, True)
        print(config)

    except FileNotFoundError as err:
        print_msg(MSG_ERROR, 'Cannot open config file: ' + str(err))
        return package.FAILURE

    except yaml.scanner.ScannerError as err:
        print_msg(MSG_ERROR, 'Syntax error while reading config file: \n' + str(err))
        return package.FAILURE

    except ValueError as err:
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
