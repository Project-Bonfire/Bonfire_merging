"""
Parses VHDL files in order to extract the relevant parts for NW and TB generation

Copyright (C) 2016 - 2017 Karl Janson, Siavoosh Payandeh Azad, Behrad Niazmand

Release under the GPLv3 license:
https://www.gnu.org/licenses/gpl-3.0.en.html
"""

import re
from Scripts.include.misc.helper_func import *
from Scripts.include.misc.package import *

STATE_OUTSIDE_ENTITY = 0
STATE_INSIDE_ENTITY = 1
STATE_INSIDE_GENERIC = 2
STATE_INSIDE_PORT = 3


def parse_entity(file_contents):
    # Find the entity block
    lines = file_contents.splitlines()

    state = STATE_OUTSIDE_ENTITY

    component_name = ''
    generics = list()

    for line in lines:

        if state == STATE_OUTSIDE_ENTITY:
            if re.match('^\s*entity', line):
                state = STATE_INSIDE_ENTITY
                component_name = line.split()[1]

        elif state == STATE_INSIDE_ENTITY:
            if re.match('^\s*generic', line):
                state = STATE_INSIDE_GENERIC

        elif state == STATE_INSIDE_GENERIC:
            result = re.search('^\s*[a-zA-Z0-9_]+\s*:\s*[a-zA-Z0-9_ ()]+', line)
            if result:
                print(result.group())

        if re.match('^\s*port', line):
            state = STATE_INSIDE_PORT

    print(component_name)
    print(generics)


def parse_file(top_module_file):
    vhdl_file = os.path.join(package.RTL_DIR, top_module_file)

    vhdl_parts = dict()

    with open(vhdl_file) as vhdl_top_module:
        file_contents = vhdl_top_module.read()

    parse_entity(file_contents)
    # print(file_contents[0])

    # print(file_contents)
    return 0


def parse_vhdl(config):

    # We assume the last file in the list to be the top module for the unit
    routers_top_module = config['router'][-1]
    ni_pe_top_module = config['ni_pe'][-1]
    if 'packet_injector' in config:
        packet_injector_top_module = config['packet_injector'][-1]

    print(parse_file(routers_top_module))
