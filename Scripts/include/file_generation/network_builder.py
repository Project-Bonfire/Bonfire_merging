"""
Implements files for generating network files

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
from Scripts.include.file_generation.vhdl_generation import *


def process_component_connections(components):
    """
    Extract interfaces for network components and lists signals for connecting them together
    :param components: List containing different network components
    :return: Dictionary containing signals
    """

    inter_router_ports = ['_n', '_e', '_w', '_s']

    router = components['router']
    ni_pe = components['ni_pe']

    ni_router_signals = dict()
    inter_router_signals = dict()
    general_router_signals = dict()
    general_ni_signals = dict()

    # Sort router signals based on connection type
    for signal in router.get_port():
        signal_port = signal['name'][signal['name'].rfind('_'):]

        if signal_port in inter_router_ports:
            inter_router_signals[signal['name'][:signal['name'].rfind('_')]] = deepcopy(signal)

        elif signal_port == '_l':
            ni_pe_sig_exists = False

            for ni_sig in ni_pe.get_port():
                if signal['name'][:signal['name'].rfind('_')] == ni_sig['name']:
                    ni_pe_sig_exists = True
                    break

            if ni_pe_sig_exists:
                ni_router_signals[signal['name'][:signal['name'].rfind('_')]] = deepcopy(signal)
            else:
                raise ValueError('Error connecting signal ' + signal['name'] + '. Signals does not exist on PE side.')

        else:
            general_router_signals[signal['name'][:signal['name'].rfind('_')]] = deepcopy(signal)

    # Sort NI / PE signals based on connection
    for signal in ni_pe.get_port():
        if signal['name'] not in ni_router_signals.keys():
            general_ni_signals[signal['name']] = deepcopy(signal)

    conn_if = dict(
        ni_router=ni_router_signals,
        inter_router=inter_router_signals,
        general_ni=general_ni_signals,
        general_router=general_router_signals
    )

    return conn_if


def build_network(components, output_dir, args, logging):

    vhdl_parts = dict()

    conn_if = process_component_connections(components)

    # get_component_parts(components['router'])
    vhdl_parts['header'] = generate_file_header('Project Bonfire Network File', 3)
    vhdl_parts['entity'] = generate_file_entity('network', None, None)
    vhdl_parts['arch'] = generate_file_arch('network', 3, components, conn_if)

    vhd_file_contents = vhdl_parts['header'] + vhdl_parts['entity'] + vhdl_parts['arch']

    # Save the file
    with open(output_dir + '/network.vhd', 'w') as vhd_file:
        vhd_file.write(vhd_file_contents)

