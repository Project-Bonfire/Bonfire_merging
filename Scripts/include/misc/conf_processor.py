"""
Reads and processes the configuration files for desingns

Copyright (C) 2016 - 2017 Karl Janson, Siavoosh Payandeh Azad, Behrad Niazmand

Release under the GPLv3 license:
https://www.gnu.org/licenses/gpl-3.0.en.html
"""

import sys
from Scripts.include.misc.helper_func import *
from Scripts.include.misc.package import *

try:
    import yaml

except ImportError as e:
    yaml = None
    print_msg(MSG_ERROR, 'Module pyyaml is not installed. Run \'pip3 install pyyaml\' to install it')
    raise ImportError(e)


def extract_config_path(args):
    """
    Calculates a config directory based on the script's arguments
    :param args: ArgParser instance
    :return:     Directory for the configuration files
    """

    if args.simulate:
        directory = package.SIM_CONF_DIR

    elif args.asic:
        directory = package.ASIC_CONF_DIR

    elif args.fpga:
        directory = package.FPGA_CONF_DIR

    else:
        raise ValueError("Unknown config type. How did we get here???")

    return directory


# def read_config(config_dir, config_name):
#     config = yaml.load(os.pathconfig_name)

