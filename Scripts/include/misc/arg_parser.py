"""
Library for parsing the arguments of the script

Copyright (C) 2016 - 2017 Karl Janson, Siavoosh Payandeh Azad, Behrad Niazmand

Release under the GPLv3 license:
https://www.gnu.org/licenses/gpl-3.0.en.html
"""

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

    exec_type_group.add_argument('--asic', '-a', type=str, required=False, metavar='DESIGN_CONFIG',
                                 help='Synthesize design stored in DESIGN_CONFIG for ASIC ' +
                                      colorize_text(True, False, 'NOT IMPLEMENTED YET', package.COLOR_RED))

    exec_type_group.add_argument('--fpga', '-f', type=str, required=False, metavar='DESIGN_CONFIG',
                                 help='Synthesize design stored in DESIGN_CONFIG for FPGA ' +
                                      colorize_text(True, False, 'NOT IMPLEMENTED YET', package.COLOR_RED))

    parser.add_argument('--debug', '-d', action='store_true', required=False,
                        help='Enable script debugging')

    # Parse the arguments
    args = parser.parse_args()

    if args.asic or args.fpga:
        raise ValueError('Requested functionality not yet implemented')

    return args
