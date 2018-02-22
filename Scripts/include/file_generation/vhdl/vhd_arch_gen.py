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

from Scripts.include.file_generation.vhdl.general_functions import *
from Scripts.include.file_generation.vhdl.generic_parser import *


def generate_signal_list(conn_if, node_count, ident_level):

    group_size = 3

    comment_dict = dict(
        general_ni='General PE Signals',
        ni_router='Connections Between NI and Router',
        inter_router='Inter-Router Connections',
        general_router='General Router Signals'
    )

    signal_list_str = gen_multi_line_comment('Signal Declarations\nNOTE: Not all of the signals below are actually used')

    for sig_type, signals in sorted(conn_if.items()):

        # Generate a comment describing the current signal group that is being processed
        if sig_type not in comment_dict.keys():
            raise ValueError('Unknown signal group... This should never happen. Something went REALLY wrong.')

        else:
            signal_list_str += '\n-- ' + comment_dict[sig_type] + '\n'

        # Generate signals for the current signal group
        for _, signal in sorted(signals.items()):

            # Do not declare clock and reset signals
            if signal['name'] not in CLK_RST_SIG_NAMES:

                # Generate a signal for each node
                signal_name_list = [signal['name'] + '_' + str(node) for node in range(node_count)]

                signal_list_str += process_lines_into_string(signal_name_list, group_size=group_size,
                                                             prefix=ident(ident_level) + 'signal ',
                                                             suffix=' : ' + signal['type'] + ';\n',
                                                             block_end_newline=True)

    return signal_list_str


def generate_port_maps(component_list, node_count, ident_level, noc_size):

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
            raise ValueError('Unknown component type... This should never happen. Something went REALLY wrong.')
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
                signal_suffix = '_' + str(node_num) if signal['name'] not in CLK_RST_SIG_NAMES else ''

                signal_name_list.append(signal['name'] + signal_suffix)

            port_map_signals = process_lines_into_string(signal_name_list, group_size=group_size,
                                                         prefix='\n' + ident(ident_level + 2),
                                                         suffix=',', block_end_newline=True)[:-2] + '\n'

            port_map_str += port_map_signals + ident(ident_level + 1) + ');'
            generic_map_str += generic_map_signals + ident(ident_level + 1) + ');'

            components_port_map_str += component_instantiation_line + generic_map_str + '\n' + port_map_str + '\n\n'

    return components_port_map_str


def build_components(component_list, noc_size, ident_level):

    comment_dict = dict(
        ni_pe='-- Processing Element',
        router='-- Router'
    )

    component_instantiation_list = [gen_multi_line_comment('Component Declarations')]

    for component_type, component in sorted(component_list.items()):

        # Insert comment describing the component
        if component_type not in comment_dict.keys():
            raise ValueError('Unknown component type... This should never happen. Something went REALLY wrong.')
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
        if component.get_port:

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
            raise RuntimeError('Tried to read port values, but they were empty. Something\'s wrong...')

        # Build the component declaration
        component_list.append(generic_str)
        component_list.append(port_str)
        component_list.append('end component;')

        component_str = process_lines_into_string(component_list)

        component_instantiation_list.append(component_str)

    # All components processed. Build the components block.
    component_instantiation_str = process_lines_into_string(component_instantiation_list)

    return component_instantiation_str

