"""
Constant declarations for the Bonfire script

Copyright (C) 2016 - 2017 Karl Janson, Siavoosh Payandeh Azad, Behrad Niazmand

Release under the GPLv3 license:
https://www.gnu.org/licenses/gpl-3.0.en.html
"""

import os

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
ASIC_DIR = TMP_DIR + '/asic_temp'
FPGA_DIR = TMP_DIR + '/fpga_temp'
LOG_DIR = TMP_DIR + '/logs'
TRACE_DIR = TMP_DIR + '/traces'

# Configurations
CONFIG_DIR = PROJECT_ROOT + '/Configs'
COMPONENT_CONF_DIR = CONFIG_DIR + '/components'
SIM_CONF_DIR = CONFIG_DIR + '/sim'
ASIC_CONF_DIR = CONFIG_DIR + '/asic'
FPGA_CONF_DIR = CONFIG_DIR + '/fpga'

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
