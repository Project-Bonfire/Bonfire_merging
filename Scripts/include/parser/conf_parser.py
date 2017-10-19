"""
Reads and processes the configuration files for designs

Copyright (C) 2016 - 2017 Karl Janson, Siavoosh Payandeh Azad, Behrad Niazmand

Release under the GPLv3 license:
https://www.gnu.org/licenses/gpl-3.0.en.html
"""

import yaml
from Scripts.include.misc.helper_func import *
from Scripts.include.misc.package import *


def extract_config_path(args):
    """
    Calculates a config directory based on the script's arguments
    :param args: ArgParser instance
    :return:     Directory for the configuration files
    """

    if args.simulate:
        config_dir = package.SIM_CONF_DIR
        config_name = args.simulate
        exec_mode = package.EXEC_TYPE_SIMUL

    elif args.asic:
        config_dir = package.ASIC_CONF_DIR
        config_name = args.asic
        exec_mode = package.EXEC_TYPE_ASIC

    elif args.fpga:
        config_dir = package.FPGA_CONF_DIR
        config_name = args.fpga
        exec_mode = package.EXEC_TYPE_FPGA

    else:
        raise ValueError("Unknown config type. How did we get here???")

    config_file = os.path.join(config_dir, config_name + '.yml')

    return config_file, exec_mode


def check_file_format(yaml_config, config_file, exec_mode, top_level):
    """
    Checks if all required fields exist in the YAML file
    :param yaml_config: (dictionary) Top level configuration read from a YAML file
    :param config_file: (str)        Name of the configuration file
    :param exec_mode:       (int)  Mode of execution (simulate, asic, fpga)
    :param top_level:   (bool)       If we are checking the top level if the main config file
                                     (while calling the function from outside of this function
                                     it should be always True)
    :return:                         None
    """
    if exec_mode == package.EXEC_TYPE_SIMUL:
        if top_level:
            list_of_elements = package.TOP_LEVEL_SIMUL_YAML_LISTS

        else:
            list_of_elements = package.SIMULATION_CONFIG_PARAMS

        for list_name in list_of_elements:
            if list_name not in yaml_config or yaml_config[list_name] is None:
                raise ValueError(list_name + ' not specified in loaded configuration! (' + config_file + ')')

            elif list_name == 'simulation_config':
                check_file_format(yaml_config['simulation_config'], config_file, exec_mode, False)

    else:
        raise RuntimeError('Ended up in the an unimplemented mode during \'check_file_format()\'!')


# def read_config(config_dir, config_name):
def read_config(config_file, exec_mode, top_level_conf, debug):
    """
    Recursively read a configuration from a YAML file
    :param config_file:     (str)  Path to the YAML configuration file to read
    :param exec_mode:       (int)  Mode of execution (simulate, asic, fpga)
    :param top_level_conf:  (bool) If we are checking the top level if the main config file
                                   (while calling the function from outside of this function
                                   it should be always True)
    :param exec_mode:       (bool) Weather we should print debugging information
    :return:                (Dictionary) Contains the configuration that was read
    """

    config = dict()
    files_to_add = list()

    with open(config_file) as yaml_file:
        yaml_config = yaml.load(yaml_file)

        try:
            if top_level_conf:

                # Test if all required fields are available
                check_file_format(yaml_config, config_file, exec_mode, True)

                # From this point all we can assume all the needed fields exist in the file
                # Recursively read the configuration
                config['simulation_config'] = yaml_config['simulation_config']
                config['network_template'] = yaml_config['network_template']
                config['router'] = read_config(os.path.join(package.ROUTERS_CONF_DIR,
                                                            yaml_config['router'] + '.yml'),
                                               exec_mode, False, debug)['files']
                config['ni_pe'] = read_config(os.path.join(package.NI_PE_CONF_DIR,
                                                           yaml_config['ni_pe'] + '.yml'),
                                              exec_mode, False, debug)['files']

                # If a packet injector is defined, we use this in the TB,
                # otherwise we will just instantiate the component there and expect things to work out on their own
                # (useful for the PE for example)
                if 'packet_injector' in yaml_config:
                    config['packet_injector'] = read_config(os.path.join(package.PACKET_INJECTOR_CONF_DIR,
                                                                         yaml_config['packet_injector'] + '.yml'),
                                                            exec_mode, False, debug)['files']

            if 'files' in yaml_config:
                for file in yaml_config['files']:
                    files_to_add.append(file)

            if files_to_add:
                config['files'] = files_to_add

        except TypeError:
            raise ValueError('Configuration file seems to be empty?!?!?! (' + config_file + ')')

    if debug:
        print_msg(MSG_DEBUG, 'Config:' + str(config))

    return config



