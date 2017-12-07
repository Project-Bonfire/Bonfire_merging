"""
Implements VHDL file arvhitecture generation

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

from Scripts.include.file_generation.vhdl.generic_functions import *


def generate_signal_list(conn_if, node_count):

    group_size = 3

    comment_dict = dict(
        general_ni='General PE Signals',
        ni_router='Connections Between NI and Router',
        inter_router='Inter-Router Connections',
        general_router='General Router Signals'
    )

    signal_list_str = gen_multi_line_comment(' Signal Declarations\n')

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

                signal_list_str += process_lines_into_string(signal_name_list, group_size=group_size, prefix='signal ',
                                                             suffix=' : ' + signal['type'] + ';\n')

    return signal_list_str


def generate_port_maps(component_list, node_count):

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

    for component_type, component in sorted(component_list.items()):

        if component_type not in component_names.keys():
            raise ValueError('Unknown component type... This should never happen. Something went REALLY wrong.')
        else:
            components_port_map_str += '\n' + comment_dict[component_type] + '\n'

        for node_num in range(node_count):

            # Generate a comment describing the current signal group that is being processed
            component_instantiation_line = component_names[component_type] + \
                                           str(node_num) + ': ' + component.get_name() + '\n'

            generic_map_str = '\tgeneric map ('
            port_map_str = '\n\tport map ('

            # Process generic map
            generic_map_str += '<placeholder>);\n'

            # Process port map
            signal_name_list = [signal['name'] for signal in component.get_port()]

            port_map_signals = process_lines_into_string(signal_name_list, group_size=group_size,
                                                         prefix='\n\t\t', suffix=',')[:-2] + '\n'

            port_map_str += port_map_signals + '\t);'

            components_port_map_str += component_instantiation_line + generic_map_str + port_map_str + '\n\n'

    return components_port_map_str


def gen_component_decl(addr, noc_size, component):

    inst_str = 'component ' + component.get_name() + ' is\n\n'

    if component.get_generic:
        inst_str += '\tgeneric (\n'

        for i, signal in enumerate(component.get_generic()):
            signal_str = '\t\t' + signal['name'] + ' : ' \
                         + signal['type'] + ' := '

            if signal['name'] == 'current_address':
                signal_str += str(addr)

            elif signal['name'] == 'cx_rst':
                signal_str += str(cx_rst_calculator(addr, noc_size))

            else:
                signal_str += signal['name']
            # signal['name']

            if i < len(component.get_generic()) - 1:
                signal_str += ';\n'
            else:
                signal_str += '\n\t);\n\n'

            inst_str += signal_str

    # port (
    #   <signal declaration 1>;
    #   <signal declaration 2>;
    #   <signal declaration n>
    # );
    if component.get_port:
        inst_str += '\tport (\n'

        for i, signal in enumerate(component.get_port()):
            signal_str = '\t\t' + signal['name'] + ' : ' \
                         + signal['direction'] + ' ' \
                         + signal['type']

            if i < len(component.get_port()) - 1:
                signal_str += ';\n'
            else:
                signal_str += '\n\t);\n\n'

            inst_str += signal_str

    else:
        raise RuntimeError('Tried to read port values, but they were empty. Something\'s wrong...')

    # End component;
    inst_str += 'end component;\n'

    return inst_str


def build_components(component_list, noc_size):

    components_str = '\n' + gen_multi_line_comment('Component Declarations')

    # Router instantiation
    components_str += '\n-- Router\n'
    components_str += gen_component_decl(0, noc_size, component_list['router'])

    # NI_PE instantiation
    components_str += '\n-- NI / PE\n'
    components_str += gen_component_decl(0, noc_size, component_list['ni_pe'])

    return components_str

