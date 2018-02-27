"""
Constant declarations for the Bonfire script

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

import os
from Scripts.include.file_generation.vhdl.general_functions import *

EXEC_TYPE_SIMUL = 0
EXEC_TYPE_SYNTH = 1
EXEC_TYPE_FPGA = 2

FAILURE = 1
SUCCESS = 0

# Color definitions
COLOR_GREY = '\033[90m'
COLOR_RED = '\033[91m'
COLOR_GREEN = '\033[92m'
COLOR_YELLOW = '\033[93m'
COLOR_BLUE = '\033[94m'
COLOR_MAGENTA = '\033[95m'
COLOR_CYAN = '\033[96m'
COLOR_END = '\033[0m'
TEXT_TYPE_BOLD = '\033[1m'
TEXT_TYPE_UNDERLINED = '\033[4m'

# Directory paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))[:-21]

# Better safe than sorry
os.chdir(PROJECT_ROOT)

# Temporary directory for storing simulation files
TMP_DIR = PROJECT_ROOT + '/tmp'
SIMUL_DIR = TMP_DIR + '/simul_temp'
SYNTH_DIR = TMP_DIR + '/synth_temp'
FPGA_DIR = TMP_DIR + '/fpga_temp'
LOG_DIR = TMP_DIR + '/logs'

# Configurations
CONFIG_DIR = PROJECT_ROOT + '/Configs'
COMPONENT_CONF_DIR = CONFIG_DIR + '/components'
ROUTERS_CONF_DIR = COMPONENT_CONF_DIR + '/routers'
NI_PE_CONF_DIR = COMPONENT_CONF_DIR + '/ni_pe'
PACKET_INJECTOR_CONF_DIR = COMPONENT_CONF_DIR + '/packet_injectors'
SIM_CONF_DIR = CONFIG_DIR + '/sim'
SYNTH_CONF_DIR = CONFIG_DIR + '/synth'
FPGA_CONF_DIR = CONFIG_DIR + '/fpga'

TOP_LEVEL_SIMUL_YAML_LISTS = (
    'simulation_config',
    'router',
    'ni_pe',
)

SIMULATION_CONFIG_PARAMS = (
    'network_size',
    'simulation_time'
)

# Design related files
RTL_DIR = PROJECT_ROOT + '/RTL'
ROUTER_RTL_DIR = RTL_DIR + '/Router'
NI_RTL_DIR = RTL_DIR + '/NI'
PROCESSOR_RTL_DIR = RTL_DIR + '/Processor'


DEFAULT_NOC_SIZE = 2

ROUTER_DEFAULTS = dict(
    current_address=0,
    shmu_address=0,
    reserved_address=0,
    flag_address=0,
    counter_address=0,
    reconfiguration_address=0,
    self_diagnosis_address=0
)

"""
Describes and action which should be done to generics when generic map is analyzed.
Keys in the dict below represent the generic names.

Each generic will be called as a function with the following parameters:
    name: name of the generic
    node_id: ID if the current node
    network_size: size of the network

Adding new generics:
* return a constant (or easily calculable value): use a lambda function.
* using a real function: specify the name of the function (without parameter declaration)
"""

GENERIC_DECISION_LIST = dict(
    # General network_component parameters
    current_address=lambda name, node_id, network_size: node_id,
    noc_size=lambda name, node_id, network_size: name,
    data_width=lambda name, node_id, network_size: name,
    noc_size_x=lambda name, node_id, network_size: network_size,

    # Fault managements
    shmu_address=lambda name, node_id, network_size: name,
    self_diagnosis_address=lambda name, node_id, network_size: name,
    reconfiguration_address=lambda name, node_id, network_size: name,
    healthy_counter_threshold=lambda name, node_id, network_size: name,
    faulty_counter_threshold=lambda name, node_id, network_size: name,
    counter_depth=lambda name, node_id, network_size: name,

    # NI connection
    reserved_address=lambda name, node_id, network_size: name,
    flag_address=lambda name, node_id, network_size: name,
    counter_address=lambda name, node_id, network_size: name,
    current_x=current_x_calculator,
    current_y=current_y_calculator,
    ni_depth=lambda name, node_id, network_size: 32,  # TODO: Make it parameterizable
    ni_counter_size=lambda name, node_id, network_size: 5,  # TODO: It should be log2 if ni_depth

    # Router configuration
    rxy_rst=lambda name, node_id, network_size: 10,  # TODO: CHANGING ROUTING BITS IS NOT IMPLEMENTED
    cx_rst=cx_rst_calculator
)

