#!/usr/bin/python3

"""
The main simulation / synthesis script of the Bonfire project

Copyright (C) 2016 - 2019 Karl Janson, Siavoosh Payandeh Azad, Behrad Niazmand

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

from Scripts.include.misc import arg_parser
from Scripts.include.misc.Logger import Logger
from Scripts.include.misc.ScreenLogger import ScreenLogger
from Scripts.include.parser.conf_parser import *
from Scripts.include.parser.vhdl_parser import *
from Scripts.include.file_generation.network_builder import *


try:
    import yaml

except ImportError as e:
    yaml = None
    print_msg(SEVERITY_ERROR,
              'Module pyyaml is not installed. Run \'pip3 install pyyaml\' to install it')
    raise ImportError(e)

TRACE_FILE = LOG_DIR + '/error.log'


def main():
    """
    Initializes the scripts and runs the actual program if initialization is successful
    :return: 1 in case of an error, 0 otherwise
    """

    # Parse command line arguments
    args = arg_parser.parse()

    # Check if the temporary folder exists. If it does, clear it, if not, create it.
    check_dir(package.LOG_DIR, True, args.debug)

    # Set up logging

    try:
        sys.stderr = Logger(TRACE_FILE, sys.__stderr__)

        logger = ScreenLogger(args.debug,
                              LOG_DIR + '/console_' +
                              str(time.time()) + '.log',
                              LOG_DIR + '/bonfire_' + str(time.time()) + '.log')
        sys.stdout = logger

    except (PermissionError, FileNotFoundError) as err:
        raise FileNotFoundError('Cannot open logfile: ' + str(err))

    # Read configurations
    config_file, exec_mode = extract_config_path(args)

    logger.blue_info('Reading config files...')

    try:
        config = read_config(config_file, exec_mode, True, logger)

    except FileNotFoundError as err:
        raise FileNotFoundError('Cannot open config file:' + str(err))

    except yaml.scanner.ScannerError as err:
        raise FileNotFoundError(
            'Syntax error while reading config file: \n' + str(err))

    # Parse the VHDL files for building the NW file and the TB#
    logger.blue_info('Parsing VHDL files...')
    components = parse_vhdl(config, False, logger)

    # # Get the output directory
    # output_dir = get_output_path(exec_mode, logger)

    # logger.blue_info('Building the design file...')
    # design_path = os.path.join(output_dir, 'design.vhd')

    # build_vhdl(components, design_path, config, 'design', True, logger)

    # logger.blue_info('Processing generated design...')

    # config['design'] = [design_path]
    # design = parse_vhdl(config, True, logger)

    # if args.simulate:
    #     tb_path = os.path.join(output_dir, 'design.vhd')
    #     logger.blue_info('Building testbench...')

    #     build_vhdl(design, tb_path, config, 'testbench', False, logger)


"""
Execution starts here
"""
if __name__ == '__main__':

    # Test for Python3
    if sys.version_info[0] == 2:
        print_msg(SEVERITY_ERROR, 'This script needs Python version 3 to run!')
        sys.exit(package.FAILURE)

    # Run the code

    try:
        main()

    except (RuntimeError, OSError, ValueError, PermissionError, FileNotFoundError) as err:
        print_msg(SEVERITY_ERROR, str(err))
        sys.exit(package.FAILURE)

sys.exit(package.SUCCESS)
