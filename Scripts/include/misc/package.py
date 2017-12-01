"""
Constant declarations for the Bonfire script

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
TRACE_DIR = TMP_DIR + '/traces'

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

ROUTER_DEFAULTS = dict(
    current_address=0,
    shmu_address=0,
    reserved_address=0,
    flag_address=0,
    counter_address=0,
    reconfiguration_address=0,
    self_diagnosis_address=0
)

# # Subfolders
# SCRIPTS_DIR = PROJECT_ROOT + '/Scripts'
# TEST_DIR = PROJECT_ROOT + '/Test'
# ROUTER_RTL_DIR = PROJECT_ROOT + '/RTL/Router'
# IMMORTAL_CHIP_DIR = PROJECT_ROOT + '/RTL/Chip_Designs/archive/IMMORTAL_Chip_2017/With_checkers'
# IMMORTAL_CHIP_FI_DIR = PROJECT_ROOT + '/RTL/Chip_Designs/IMMORTAL_Chip_2017/network_files'
# FAULT_MANAGEMENT_RTL_DIR = PROJECT_ROOT + '/RTL/Fault_Management'
# CHECKERS_DIR = '/Checkers/Modules_with_checkers_integrated/All_checkers'
#
#
# # Flow control suffixes
# CREDIT_BASED_SUFFIX = 'credit_based'
#
# # Script names
# NET_GEN_SCRIPT = 'network_gen_parameterized'
# NET_TB_GEN_SCRIPT = 'network_tb_gen_parameterized'
# WAVE_DO_GEN_SCRIPT = 'wave_do_gen'
# SIMUL_DO_SCRIPT = 'simulate.do'
# RECEIVED_TXT_PATH = 'received.txt'
# SENT_TXT_PATH = 'sent.txt'
# LATENCY_CALCULATION_PATH = 'calculate_latency.py'
#
# # Default simulation configuration
# program_argv = {
#         'network_dime':    4,
#         'credit_based_FC': False,
#         'add_parity':      False,
#         'add_checkers':    False,
#         'packet_drop':     False,
#         'add_NI':          -1,
#         'NI_Test':         False,
#         'add_FI':          False,
#         'add_FC':          False,
#         'add_FO':          False,
#         'add_SHMU':        False,
#         'rand':            -1,
#         'BR':              -1,
#         'PS':              [3,8],
#         'sim':             -1,
#         'end':             -1,
#         'lat':             False,
#         'debug':           False,
#         'trace':           False,
#         'verilog':         False,
#         'command-line':    False,
#     }
#
# # Debug mode is off by default
# DEBUG = False
#
# # fault injection settings
# FAULT_RANDOM_SEED = None        # set to None if you want random randomness
# Fault_Per_Second = 90000000
# HIGH_FAULT_RATE = 1.1
# MEDIUM_FAULT_RATE = 1
# LOW_FAULT_RATE = 0.9
#
# MTB_INTERMITTENT_BURST = 100   # mean time between intermittent fault bursts
# EVENTS_PER_BURST = 10
