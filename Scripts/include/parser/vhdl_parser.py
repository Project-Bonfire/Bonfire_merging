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

from copy import deepcopy
from Scripts.include.misc.helper_func import *
from Scripts.include.misc.package import *
from Scripts.include.components.noc_component import NoCComponent

TYPE_ROUTER = 'router'
TYPE_NI_PE = 'ni_pe'
TYPE_INJECTOR = 'packet_injector'


def process_signal_list(signals, vhd_file, logging, is_port):
    """
    Processes a list of signals
    :param signals:     List of signals to be processes
    :param vhd_file:    VHDL file to process
    :param logging:     Logger instance
    :param is_port:     True if the signals passed to this method belong to a port,
                        False, if they are part of generic
    :return:            List containing parsed signal entries
    """

    # Generic was empty
    if signals == ['']:
        return []

    signal_list = list()

    # Process signals
    for signal in signals:
        signal_components = dict()

        # Extract initialization
        try:

            if ':=' in signal:
                signal, init_value = signal.split(':=')
                signal_components['init_value'] = init_value.strip()

            # Extract type declaration
            if ':' not in signal:
                raise ValueError()

            signal_name_list, type_declaration = signal.split(':')

            # Split name list
            signal_name_list = signal_name_list.strip().split(',')
            type_declaration = type_declaration.strip()

        except ValueError:
            raise RuntimeError('Syntax error in ' + vhd_file
                               + ': ' + signal.strip())

        # Find direction declaration
        in_location = word_in_string('in', type_declaration)
        out_location = word_in_string('out', type_declaration)

        # Extract signal direction and type
        if in_location is None and out_location is None and is_port:
            raise RuntimeError('Syntax error in ' + vhd_file
                               + '. No direction is specified in port: ' + signal.strip())

        if in_location is None and out_location is not None:
            signal_components['direction'] = type_declaration[:out_location.end()].strip()
            signal_components['type'] = type_declaration[out_location.end():].strip()

        elif in_location is not None and out_location is None:
            signal_components['direction'] = type_declaration[:in_location.end()].strip()
            signal_components['type'] = type_declaration[in_location.end():].strip()

        elif in_location is not None and out_location is not None:
            raise RuntimeError('Syntax error in ' + vhd_file
                               + '. Cannot determine signal direction: ' + signal.strip())

        else:
            signal_components['type'] = type_declaration.strip()

        # Process signal name list
        for signal_name in signal_name_list:
            signal_components['name'] = signal_name.strip()

            # Add processed signal to list
            signal_list.append(deepcopy(signal_components))

            logging.debug('Found signal: ' + signal_components['name'])

    print(signal_list)
    return signal_list


def extract_entity_components(vhd_file, logging):
    """
    Parse VHDL in order to extract the entity's configuration.
    :param vhd_file:    VHDL file to parse
    :param logging:     Logger instance
    :return:            [Name of the entity, generic signals, port signals]
    """

    with open(vhd_file, 'r') as vhd:
        buffer = ''

        # Remove comments, replace newlines with space for easier processing
        for line in vhd:
            line = line.partition('--')[0].replace('\n', ' ').replace('\r', '')
            buffer = buffer + line

        # Change the file to all lower case for easier processing (VHDL is case insensitive)
        buffer = buffer.lower()

        # Find 'entity'
        entity_location = word_in_string('entity', buffer)

        if entity_location is None:
            raise RuntimeError('Cannot find entity declaration in ' + vhd_file)
        else:
            entity_location = entity_location.end()

        # Find 'architecture'
        architecture_location = word_in_string('architecture', buffer)

        if architecture_location is None:
            raise RuntimeError('Cannot find architecture in ' + vhd_file)
        else:
            architecture_location = architecture_location.start()

        # Extract the entity
        entity = buffer[entity_location:architecture_location]

        is_location = word_in_string('is', entity)

        # Find 'is'
        if is_location is None:
            raise RuntimeError('Malformed entity declaration in ' + vhd_file + ' (cannot find \'is\')')
        else:
            is_span = is_location.span()

        # Find and set entity name
        entity_name = entity[:is_span[0]].strip()
        logging.debug('Entity name: ' + entity_name)

        # Find 'end'
        end_location = word_in_string('end', entity)

        if end_location is None:
            raise RuntimeError('Malformed entity declaration in ' + vhd_file + ' (cannot find \'end\')')
        else:
            end_start = end_location.start()

        # Extract entity's body
        entity = entity[is_span[1]:end_start]

        # Locate generic and port declaration in the string
        generic_location = word_in_string('generic', entity)
        port_location = word_in_string('port', entity)

        # Extract generic and port
        if port_location is None:
            raise RuntimeError('No port definition found int he entity of the file ' + vhd_file + '!')

        # Entity contains only port definition
        if generic_location is None:
            generic = 'generic ();'
            port = entity

        else:
            # Generic is defined first
            if generic_location.end() < port_location.start():
                generic = entity[generic_location.end():port_location.start()]
                port = entity[port_location.end():]

            # Port is defined first
            else:
                generic = entity[port_location.end():].strip()
                port = entity[port_location.end():generic_location.start()].strip()

        # Remove extra parenthesis and split signals

        try:
            generic = generic[generic.find('(') + 1:generic.rfind(')')].split(';')

        except ValueError:
            raise RuntimeError('Syntax error in ' + vhd_file
                               + ': Format error in generic definition. (Check semicolons and brackets)')

        try:
            port = port[port.find('(') + 1:port.rfind(')')].split(';')

        except ValueError:
            raise RuntimeError('Syntax error in ' + vhd_file
                               + ': Format error in port definition. (Check semicolons and brackets)')

        logging.debug('Processing generic')
        generic_signal_list = process_signal_list(generic, vhd_file, logging, False)

        logging.debug('Processing port')
        port_signal_list = process_signal_list(port, vhd_file, logging, True)

        return [entity_name, generic_signal_list, port_signal_list]


def parse_component(config, component_type, logging):
    """
    Parses a specific component.
    :param config:          Configuration extracted from the config file
    :param component_type:  Type of the component
    :param logging:         Logger instance
    :return:                Instance of NoCComponent, each representing one component in the NoC
    """

    # Parse the top module's VHDL in order to extract the interface
    component = NoCComponent()
    router_top_module = os.path.join(RTL_DIR, config[component_type][-1])
    logging.debug('Processing component\'s top module:' + router_top_module)
    entity_name, generic_signal_list, port_signal_list = \
        extract_entity_components(router_top_module, logging)

    # Apply parameters to the component
    component.set_name(entity_name)
    component.set_generic(generic_signal_list)
    component.set_port(port_signal_list)

    return component


def parse_vhdl(config, logging):
    """
    Finds top modules of each network component, parses the VHDL and returns all NoC components.
    :param config:  Configuration extracted from the config file
    :param logging: Logger instance
    :return:        List of NoCComponent instances, each representing one component in the NoC
    """

    # Assume the last file in the list to be the top module for the unit
    network_components = dict()

    # Router
    logging.debug('Processing router')
    network_components['router'] = \
        parse_component(config, TYPE_ROUTER, logging)

    # NI / PE
    logging.debug('Processing NI / PE')
    network_components['ni_pe'] = network_components['router'] = \
        parse_component(config, TYPE_NI_PE, logging)

    # Packet injector
    if 'packet_injector' in config:
        logging.debug('Processing packet injector')
        network_components['packet_injector'] = \
            network_components['router'] = parse_component(config, TYPE_INJECTOR, logging)

    return network_components
