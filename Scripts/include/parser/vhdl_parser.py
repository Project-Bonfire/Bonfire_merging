"""
Parses VHDL files in order to extract the relevant parts for NW and TB generation

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

import re
from Scripts.include.misc.helper_func import *
from Scripts.include.misc.package import *


def extract_entity_components(vhd_file):

    buffer = ''

    with open(vhd_file, 'r') as vhd:

        # Strip comments and newlines
        for line in vhd:
            line = line.partition('--')[0]
            line = line.rstrip()
            buffer = buffer + line

        # Change the file to all lower case for easier processing
        buffer = buffer.lower()

        # Check if entity exists
        if 'entity' not in buffer:
            raise ValueError('Cannot find entity declaration in ' + vhd_file)

        if 'architecture' not in buffer:
            raise ValueError('Cannot find architecture in ' + vhd_file)

        # Extract the entity
        entity = buffer.split('entity')[1].split('architecture')[0]

        if 'is' not in entity:
            raise ValueError('Malformed entity declaration in ' + vhd_file + ' (cannot find \'is\')')

        if 'end' not in entity:
            raise ValueError('Cannot find the end of entity in ' + vhd_file)

        # Extract entity name and contents (port and generic definition)
        entity_name, entity_contents = entity.split('end')[0].split('is')

        # Locate generic and port declaration in the string
        generic_loc = entity_contents.find('generic')
        port_loc = entity_contents.find('port')

        # Extract generic and port
        if port_loc == -1:
            raise ValueError('No port definition found int he entity of the file ' + vhd_file + 'stopping')

        if generic_loc == -1:
            generic = ''
            port = entity_contents.split('port')[1]

        else:
            if generic_loc < port_loc:
                generic, port = entity_contents.split('generic')[1].split('port')

            else:
                port, generic = entity_contents.split('port')[1].split('generic')


        regex = re.compile('[a-z0-0_]+\s*:\s*[a-z]*\s+[a-z0-0_]+[\(\)0-9a-z ]*\s*:?=?\s*\d*')

        generic_decl = regex.findall(generic)
        port_decl = regex.findall(port)

        # print(entity)
        # print(entity_name)
        # print(entity_contents)
        # print('port')
        # print(port)
        print(generic_decl)
        print(port_decl)

def parse_vhdl(config):

    # We assume the last file in the list to be the top module for the unit
    routers_top_module = os.path.join(ROUTER_RTL_DIR, config['router'][-1])
    ni_pe_top_module = config['ni_pe'][-1]
    if 'packet_injector' in config:
        packet_injector_top_module = config['packet_injector'][-1]

    extract_entity_components(routers_top_module)

