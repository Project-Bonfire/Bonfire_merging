"""
Implements VHDL file architecture generation

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

from Scripts.include.misc.package import *
from Scripts.include.file_generation.vhdl.general_functions import *

INTER_ROUTER_SUFFICES = ['_n', '_e', '_w', '_s']

SIGNAL_GROUP_SIZE = 3

VALID_COMOPONENT_TYPES = [
    'general_ni',
    'ni_router',
    'inter_router',
    'general_router',
    'design_signal'
]


def generate_opposite_port_name(port_name):

    if port_name == 'tx':
        opposite_name = 'rx'

    elif '_out' in port_name:
        opposite_name = port_name[:port_name.rfind('_')] + '_in'

    else:
        raise RuntimeError('Portname has unknown format. Cannot parse: ' + port_name)

    return opposite_name


def generate_connections(conn_if, node_count, ident_level):

    inter_router_ports = ['_n', '_e', '_w', '_s']

    group_size = 3

    comment_dict = dict(
        general_ni='General PE Signals',
        ni_router='Connections Between NI and Router',
        inter_router='Inter-Router Connections',
        general_router='General Router Signals',
    )

    signal_list_str = gen_multi_line_comment('Connecting signals')

    signal_list_str += '\n---- ' + comment_dict['inter_router'] + ' ----\n\n'

    connectivity_matrix = connectivity_matrix_calculator(3)

    for node, connections in sorted(connectivity_matrix.items()):

        node_connections = list()

        potential_neighbors = [node - 3, node + 1, node - 1, node + 3]

        # Find connecting signals for all nodes
        for index, connection in enumerate(connections):
            if connection is not None:
                for signal_name in sorted(conn_if['inter_router']):

                    if signal_name == 'tx' or '_out' in signal_name:
                        current_sig = signal_name + inter_router_ports[index] + '_' + str(node)

                        connecting_sig = generate_opposite_port_name(signal_name) \
                                         + list(reversed(inter_router_ports))[index] \
                                         + '_' + str(potential_neighbors[index])

                        node_connections.append(connecting_sig + ' <= ' + current_sig)

        signal_list_str += '-- ' + 'Connecting router ' + str(node) + ' outputs\n'
        signal_list_str += process_lines_into_string(sorted(node_connections),
                                                     prefix=ident(ident_level),
                                                     suffix=';\n',
                                                     block_end_newline=True)

    return signal_list_str


def generate_signal_list(conn_if, node_count, ident_level):

    sig_decl_comments = dict(
        general_ni='General PE Signals',
        ni_router='Connections Between NI and Router',
        inter_router='Inter-Router Connections',
        general_router='General Router Signals',

        design_signal='Signals connected to DUT'
    )

    signal_list_str = gen_multi_line_comment('Signal Declarations\n'
                                             'NOTE: Not all of the signals below are actually used')

    for sig_type, signals in sorted(conn_if.items()):

        # Generate a comment describing the current signal group that is being processed
        if sig_type not in VALID_COMOPONENT_TYPES:
            raise RuntimeError('(generate_signal_list) Unknown signal group... '
                               'This should never happen. Something went REALLY wrong.')

        else:
            signal_list_str += '\n-- ' + sig_decl_comments[sig_type] + '\n'

        # Generate signals for the current signal group
        for _, signal in sorted(signals.items()):

            # Do not declare clock and reset signals
            if signal['name'] not in CLK_RST_SIG_NAMES:

                signal_name_list = list()

                # For inter-router signals generate an entry for all ports
                if sig_type == 'inter_router':
                    for port in INTER_ROUTER_SUFFICES:
                        signal_name_list.append(signal['name'] + port)
                elif sig_type == 'ni_router':
                    signal_name_list.append(signal['name'] + '_ni')
                    signal_name_list.append(signal['name'] + '_l')
                else:
                    signal_name_list.append(signal['name'])

                # Have an entry for all nodes
                signal_name_list_with_node = list()
                for node in range(node_count):
                    for sig_name in signal_name_list:
                        signal_name_list_with_node.append(sig_name + '_' + str(node))

                signal_list_str += process_lines_into_string(signal_name_list_with_node, group_size=SIGNAL_GROUP_SIZE,
                                                             prefix=ident(ident_level) + 'signal ',
                                                             suffix=' : ' + signal['type'] + ';\n',
                                                             block_end_newline=True)

    return signal_list_str


def generate_port_maps(conn_if, component_list, node_count, ident_level, noc_size):

    group_size = 3

    component_names = dict(
        ni_pe='NI_',
        router='R_'
    )

    comment_dict = dict(
        ni_pe='-- Processing Elements',
        router='-- Routers'
    )

    components_port_map_str = gen_multi_line_comment('Port Maps')

    # Search for different components
    for component_type, component in sorted(component_list.items()):

        if component_type not in component_names.keys():
            raise ValueError('generate_port_maps(): Unknown component type... '
                             'This should never happen. Something went REALLY wrong.')
        else:
            components_port_map_str += '\n' + comment_dict[component_type] + '\n'

        for node_num in range(node_count):

            # Generate a comment describing the current signal group that is being processed
            component_instantiation_line = ident(ident_level) + component_names[component_type] + \
                                           str(node_num) + ': ' + component.get_name() + '\n'

            generic_map_str = ident(ident_level + 1) + 'generic map ('
            port_map_str = '\n' + ident(ident_level + 1) + 'port map ('

            # Process generic map
            signal_name_list = []

            for signal in component.get_generic():

                try:
                    generic_signal_value = str(GENERIC_DECISION_LIST[signal['name']](signal['name'], node_num, noc_size))
                except KeyError:
                    raise RuntimeError('Unknown generic signal: ' + signal['name'] + ' (in ' + component.get_name() + ')'
                                       + ' - Add a parsing rule to GENERIC_DECISION_LIST in generic_parse.py')

                generic_signal = signal['name'] + ' => ' + generic_signal_value

                # TODO: ADD SIGNAL TO FILE ENTITY

                signal_name_list.append(generic_signal)

            generic_map_signals = process_lines_into_string(signal_name_list, prefix='\n' + ident(ident_level + 2),
                                                            suffix=',', block_end_newline=True)[:-2] + '\n'

            # Process port map
            signal_name_list = []

            for signal in component.get_port():

                signal_suffix = ''

                if signal['name'] not in CLK_RST_SIG_NAMES:

                    if signal['name'] in conn_if['ni_router']:
                        signal_suffix = '_ni_' + str(node_num)

                    else:
                        signal_suffix = '_' + str(node_num)

                # signal_suffix = '_' + str(node_num) if signal['name'] not in CLK_RST_SIG_NAMES else ''

                signal_name_list.append(signal['name'] + signal_suffix)

            port_map_signals = process_lines_into_string(signal_name_list, group_size=group_size,
                                                         prefix='\n' + ident(ident_level + 2),
                                                         suffix=',', block_end_newline=True)[:-2] + '\n'

            port_map_str += port_map_signals + ident(ident_level + 1) + ');'
            generic_map_str += generic_map_signals + ident(ident_level + 1) + ');'

            components_port_map_str += component_instantiation_line + generic_map_str + '\n' + port_map_str + '\n\n'

    return components_port_map_str


def build_component_decl(component_list, noc_size, ident_level):

    comment_dict = dict(
        ni_pe='-- Processing Element',
        router='-- Router',
        packet_injector='-- Packet Injector'
    )

    component_instantiation_list = [gen_multi_line_comment('Component Declarations')]

    for component_type, component in sorted(component_list.items()):

        # Insert comment describing the component
        if component_type not in comment_dict.keys():
            raise RuntimeError('(build_component_decl) Unknown component type (' + str(component_type) + ')... '
                               'This should never happen. Something went REALLY wrong.')
        else:
            component_instantiation_list.append(comment_dict[component_type])

        # Component processing start here
        generic_list = list()
        port_list = list()

        generic_str = ''
        port_str = ''

        component_list = [ident(ident_level) + 'component ' + component.get_name() + ' is']

        # Process Generic
        if component.get_generic():
            generic = component.get_generic()

            # Measure maximum signal name length, for formatting purposes
            max_line_length = max([[len(line['name'])] for line in generic])[0]

            generic_list.append(ident(ident_level + 1) + 'generic (')

            # Process all signals in the port
            for signal in generic:
                free_space = (max_line_length - len(signal['name'])) * ' '

                init_str = '' if 'init_value' not in signal else ' := ' + signal['init_value']

                # Build signal line
                signal = [ident(ident_level + 2),
                          signal['name'], free_space, ' : ', signal['type'] + init_str + ';']

                signal_str = process_lines_into_string(signal, suffix='')

                generic_list.append(signal_str)

            generic_list[-1] = generic_list[-1][:-1]

            generic_list.append(ident(ident_level + 1) + ');')
            generic_str = process_lines_into_string(generic_list)

        # Process Port
        if component.get_port():

            port = component.get_port()

            # Measure maximum signal name length, for formatting purposes

            max_line_length = max([[len(line['name'])] for line in port])[0]

            port_list.append(ident(ident_level + 1) + 'port (')

            # Process all signals in the port
            for signal in port:
                free_space = (max_line_length - len(signal['name'])) * ' '

                # Build signal line
                signal = [ident(ident_level + 2),
                          signal['name'], free_space, ' : ', signal['direction'], ' ', signal['type'] + ';']

                signal_str = process_lines_into_string(signal, suffix='')

                port_list.append(signal_str)

            port_list[-1] = port_list[-1][:-1]

            port_list.append(ident(ident_level + 1) + ');')
            port_str = process_lines_into_string(port_list)

        else:
            raise RuntimeError('(build_component_decl)Tried to read port values, but they were empty. '
                               '(Component\'s name:)' + component.get_name()
                               + 'Something\'s wrong...')

        # Build the component declaration
        component_list.append(generic_str)
        component_list.append(port_str)
        component_list.append('end component;')

        component_str = process_lines_into_string(component_list)

        component_instantiation_list.append(component_str)

    # All components processed. Build the components block.
    component_instantiation_str = process_lines_into_string(component_instantiation_list)

    return component_instantiation_str

