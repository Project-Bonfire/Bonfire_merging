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
from Scripts.include.components.noc_component import NoCComponent


def process_signal_list(signals, is_port):
    s = list()
    # Strip the extra brackets from the signal list and split signals
    start_bracket_loc = signals.find('(') + 1
    end_bracket_loc = signals.rfind(');')

    signal_list = signals[start_bracket_loc:end_bracket_loc].split(';')

    for signal in signal_list:
        signal_components = dict()

        if ':' not in signal:
            raise ValueError('Syntax error reading signal ' + signal)

        # print(signal)

        if ':=' in signal:
            tmp, init_value = signal.split(':=')
            init_value = init_value.strip()

        else:
            tmp = signal

        name_list, tmp = tmp.split(':')
        tmp = tmp.strip()
        name_list = name_list.strip()

        print(name_list, '\\\\', tmp)

        if 'in ' in tmp or 'out ' in tmp:
            space_place = tmp.find(' ')
            print(space_place, tmp)


def extract_entity_components(vhd_file, component, logging):

    buffer = ''

    with open(vhd_file, 'r') as vhd:

        # Strip comments, empty spaces from beginning and end and newlines
        for line in vhd:
            line = line.partition('--')[0].rstrip()
            buffer = buffer + line

        # Change the file to all lower case for easier processing (VHDL is case insensitive)
        buffer = buffer.lower()

        # Check if entity exists
        if word_in_string('entity', buffer) is None:
            raise RuntimeError('Cannot find entity declaration in ' + vhd_file)

        # Check if an architecture exists
        if word_in_string('architecture', buffer) is None:
            raise RuntimeError('Cannot find architecture in ' + vhd_file)

        # Extract the entity
        entity = buffer.split('entity')[1].split('architecture')[0]

        if word_in_string('is', entity) is None:
            raise RuntimeError('Malformed entity declaration in ' + vhd_file + ' (cannot find \'is\')')

        if word_in_string('end', entity) is None:
            raise RuntimeError('Cannot find the end of entity in ' + vhd_file)

        # Extract entity name and contents (port and generic definition)
        entity_name, entity_contents = entity.split('end')[0].split('is')

        # Locate generic and port declaration in the string
        generic_loc = entity_contents.find('generic')
        port_loc = entity_contents.find('port')

        # Extract generic and port
        if port_loc == -1:
            raise RuntimeError('No port definition found int he entity of the file ' + vhd_file + 'stopping')

        if generic_loc == -1:
            generic = ''
            port = entity_contents.split('port')[1]

        else:
            if generic_loc < port_loc:
                generic, port = entity_contents.split('generic')[1].split('port')

            else:
                port, generic = entity_contents.split('port')[1].split('generic')

        print('==========')
        process_signal_list(generic, False)
        print('==========')
        process_signal_list(port, True)


        # regex = re.compile('([a-z0-0_],*\s*)+\s*:\s*[a-z]*\s*[a-z0-0_]+\s*(\(.*?\))*')
        #
        # generic_decl = regex.findall(generic)
        # port_decl = regex.findall(port)
        #
        # print(generic_decl)
        # print(port_decl)
        #
        # process_signal(generic_decl, False)
        # print('=============================')
        # process_signal(port_decl, True)


def parse_vhdl(config, logging):

    # Assume the last file in the list to be the top module for the unit
    router = NoCComponent()
    router_top_module = os.path.join(RTL_DIR, config['router'][-1])
    extract_entity_components(router_top_module, router, logging)
    logging.debug('Router\'s top module:' + router_top_module)

    ni_pe = NoCComponent()
    ni_pe_top_module = os.path.join(RTL_DIR, config['ni_pe'][-1])
    extract_entity_components(ni_pe_top_module, ni_pe, logging)
    logging.debug('Router\'s top module:' + ni_pe_top_module)

    if 'packet_injector' in config:
        packet_injector = NoCComponent
        packet_injector_top_module = os.path.join(RTL_DIR, config['packet_injector'][-1])
        extract_entity_components(packet_injector_top_module, packet_injector, logging)
        logging.debug('Router\'s top module:' + packet_injector_top_module)

