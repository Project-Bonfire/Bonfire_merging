"""
Library for parsing the arguments of the script

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
import argparse
from Scripts.include.misc import package
from Scripts.include.misc.helper_func import colorize_text


def parse():
    """
    Parses the arguments
    :return: Argparse instance containing the parameters
    """

    parser = argparse.ArgumentParser(description=colorize_text(True, True, 'Bonfire simulation / synthesis script',
                                                               package.COLOR_BLUE))

    parser._optionals.title = colorize_text(True, False, 'Optional arguments', package.COLOR_BLUE)

    exec_type = parser.add_argument_group(colorize_text(True, False, 'Execution type', package.COLOR_BLUE))

    exec_type_group = exec_type.add_mutually_exclusive_group(required=True)

    exec_type_group.add_argument('--simulate', '-s', type=str, required=False, metavar='DESIGN_CONFIG',
                                 help='Simulate the design stored in DESIGN_CONFIG')

    exec_type_group.add_argument('--synth', '-a', type=str, required=False, metavar='DESIGN_CONFIG',
                                 help='Synthesize design stored in DESIGN_CONFIG ' +
                                      colorize_text(True, False, 'NOT IMPLEMENTED YET', package.COLOR_RED))

    exec_type_group.add_argument('--fpga', '-f', type=str, required=False, metavar='DESIGN_CONFIG',
                                 help='Synthesize design stored in DESIGN_CONFIG for FPGA ' +
                                      colorize_text(True, False, 'NOT IMPLEMENTED YET', package.COLOR_RED))

    parser.add_argument('--debug', '-d', action='store_true', required=False,
                        help='Enable script debugging')

    # Display the --help message when no arguments are given
    if len(sys.argv[1:]) == 0:
        parser.print_help()
        # parser.print_usage() # for just the usage line
        parser.exit()

    # Parse the arguments
    args = parser.parse_args()

    if args.synth or args.fpga:
        raise ValueError('Requested functionality not yet implemented')

    return args
