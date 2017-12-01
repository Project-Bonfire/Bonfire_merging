"""
Implements files for parts of VHDL files

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


def generate_copyright():
    """
    Generates copytight message
    :return: string containing the copyright message
    """

    return """
-- Copyright (C) 2016 - 2017 Karl Janson, Siavoosh Payandeh Azad, Behrad Niazmand
-- 
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU General Public License as published by
-- the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
-- 
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
-- GNU General Public License for more details.
-- 
-- You should have received a copy of the GNU General Public License
-- along with this program.  If not, see <http://www.gnu.org/licenses/>.
    """


def cx_rst_calculator(node_id, network_size):
    node_x = node_id % network_size
    node_y = node_id / network_size

    c_n = 1
    c_e = 1
    c_w = 1
    c_s = 1

    if node_y == 0:
        c_n = 0

    if node_y == network_size - 1:
        c_s = 0

    if node_x == 0:
        c_w = 0

    if node_x == network_size - 1:
        c_e = 0

    return c_s * 8 + c_w * 4 + c_e * 2 + c_n


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


def generate_file_header(file_descr, noc_size):
    """
    Generates VHDL file header
    :param file_descr:  Generated file description
    :param noc_size:    Size of the network
    :return: String containing the VHDL file header for the network
    """

    return '-' * 82 + '\n'\
        + '-- ' + file_descr + '\n' \
        + '-' * 82 + '\n'\
        + generate_copyright() + '\n' \
        + '-' * 82 + '\n' \
        + '-- This file has been automatically generated. Just for you :)\n' \
        + '-- (DO NOT EDIT)\n' \
        + '-' * 82 + '\n' \
        + '-- Generated network size: ' + str(noc_size) + 'x' + str(noc_size) + '\n'


def generate_file_entity(entity_name, generic, port):
    """
    Generates an VHDL entity
    :param entity_name: Name of the entity
    :param generic:     List of generics
    :param port:        List of port signals
    :return:
    """

    return '\n\n' \
        + 'library ieee;\n' \
        + 'use ieee.std_logic_1164.all;\n' \
        + 'use IEEE.STD_LOGIC_ARITH.ALL;\n' \
        + 'use IEEE.STD_LOGIC_UNSIGNED.ALL;\n' \
        + 'USE ieee.numeric_std.ALL;\n\n' \
        + 'entity ' + entity_name + ' is\n' \
        + '\tgeneric(' + '<generic_placeholder>' + ');\n' \
        + '\tport(' + '<port_placeholder>' + ');\n' \
        + 'end ' + entity_name + ';\n\n'


def build_components(component_list, noc_size):

    # Router instantiation
    components_str = '\n-- Router\n'
    components_str += gen_component_decl(0, noc_size, component_list['router'])

    # NI_PE instantiation
    components_str += '\n-- NI / PE\n'
    components_str += gen_component_decl(0, noc_size, component_list['ni_pe'])

    return components_str


def generate_file_arch(arch_name, noc_size, component_list):
    arch_contents = ''
    arch_contents += 'architecture behavior of ' + arch_name + 'is\n'
    arch_contents += '\t' + build_components(component_list, noc_size) + '\n'
    arch_contents += 'begin\n'
    arch_contents += '\t<code_placeholder>\n'
    arch_contents += 'end ' + arch_name + ';\n'

    return arch_contents
