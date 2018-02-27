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

from Scripts.include.misc.package import *
from Scripts.include.file_generation.vhdl.vhd_file_gen import *


def process_design_connections(components):
    """
    Extract interfaces for network components and lists signals for connecting them together
    :param components:          (list) List containing different network components
    :return: Dictionary containing signals
    """

    inter_router_ports = ['_n', '_e', '_w', '_s']

    design = components['design']

    if 'packet_injector' in components:
        packet_injector = components['packet_injector']
    else:
        packet_injector = dict()

    injector_pe_signals = dict()
    inter_router_signals = dict()
    general_design_signals = dict()
    general_injector_signals = dict()

    # Sort design signals based on connection type
    for signal in design.get_port():
        print(design.get_port())
        signal_port = signal['name'][signal['name'].rfind('_'):]
        print(signal_port)

    #     if signal_port == '_l':
    #         ni_pe_sig_exists = False
    #
    #         for ni_sig in packet_injector.get_port():
    #             if signal['name'][:signal['name'].rfind('_')] == ni_sig['name']:
    #                 ni_pe_sig_exists = True
    #                 break
    #
    #         if ni_pe_sig_exists:
    #             injector_pe_signals[signal['name'][:signal['name'].rfind('_')]] = deepcopy(signal)
    #             injector_pe_signals[signal['name'][:signal['name'].rfind('_')]]['name'] = \
    #                 signal['name'][:signal['name'].rfind('_')]
    #         else:
    #             raise ValueError('Error connecting signal ' + signal['name'] + '. Signals does not exist on PE side.')
    #
    #     else:
    #         general_design_signals[signal['name'][:signal['name'].rfind('_')]] = deepcopy(signal)
    #
    # # Sort NI / PE signals based on connection
    # for signal in packet_injector.get_port():
    #     if signal['name'] not in injector_pe_signals.keys():
    #         general_injector_signals[signal['name']] = deepcopy(signal)
    #
    # conn_if = dict(
    #     ni_router=injector_pe_signals,
    #     inter_router=inter_router_signals,
    #     general_ni=general_injector_signals,
    #     general_router=general_design_signals,
    #     design_signal=[]
    # )

    # print(conn_if)

    import sys
    print('YEYEYEYEYYEYEYEYE')
    sys.exit(1)
    # return conn_if


def process_component_connections(components):
    """
    Extract interfaces for network components and lists signals for connecting them together
    :param components:          (list) List containing different network components
    :return: Dictionary containing signals
    """

    inter_router_ports = ['_n', '_e', '_w', '_s']

    router = components['router']
    ni_pe = components['ni_pe']

    ni_router_signals = dict()
    inter_router_signals = dict()
    general_router_signals = dict()
    general_ni_signals = dict()
    design_signals = dict()

    # Sort router signals based on connection type
    for signal in router.get_port():
        signal_port = signal['name'][signal['name'].rfind('_'):]

        if signal_port in inter_router_ports:
            inter_router_signals[signal['name'][:signal['name'].rfind('_')]] = deepcopy(signal)

            # Generalize signal name
            inter_router_signals[signal['name'][:signal['name'].rfind('_')]]['name'] = \
                signal['name'][:signal['name'].rfind('_')]

        elif signal_port == '_l':
            ni_pe_sig_exists = False

            for ni_sig in ni_pe.get_port():
                if signal['name'][:signal['name'].rfind('_')] == ni_sig['name']:
                    ni_pe_sig_exists = True
                    break

            if ni_pe_sig_exists:
                ni_router_signals[signal['name'][:signal['name'].rfind('_')]] = deepcopy(signal)
                ni_router_signals[signal['name'][:signal['name'].rfind('_')]]['name'] = \
                    signal['name'][:signal['name'].rfind('_')]
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
        general_router=general_router_signals,
    )

    return conn_if


def build_vhdl(components, output_file, config, entity_name, design_generation, logger):
    """
    Builds top-level VHDL code from the components
    :param components:  (dict)   Components to include in the top-module
    :param output_file: (str)    Path to the output VHDL file
    :param config:      (dict)   System configuration
    :param entity_name: (str)    Name of the generated entity
    :param design_generation:   (bool)   if the file being processed is a design file
    :param logger:      (Logger) An object providing logging functionality
    :return: None
    """

    logger.debug("VHDL file building started")

    vhdl_file_sections = dict()
    ident_level = 0

    sim_conf = config['simulation_config']

    noc_size = sim_conf['network_size'] if 'network_size' in sim_conf else DEFAULT_NOC_SIZE

    logger.debug("Analyzing component connections")

    if design_generation:
        conn_if = process_design_connections(components)
    else:
        conn_if = process_component_connections(components)

    # We will gather information needed for building the entity while we build the architecture
    logger.debug("Building file header")
    vhdl_file_sections['header'] = generate_file_header('Project Bonfire ' + entity_name.upper() + ' File', noc_size)

    logger.debug("Building file architecture")
    vhdl_file_sections['arch'] = generate_file_arch('entity_name', noc_size, components, conn_if, ident_level, logger)

    logger.debug("Building Entity")
    vhdl_file_sections['entity'] = generate_file_entity('entity_name', conn_if, design_generation, ident_level, logger)

    vhd_file_contents = vhdl_file_sections['header'] + vhdl_file_sections['entity'] + vhdl_file_sections['arch']

    # Save the file
    with open(output_file, 'w') as vhd_file:
        vhd_file.write(vhd_file_contents)


