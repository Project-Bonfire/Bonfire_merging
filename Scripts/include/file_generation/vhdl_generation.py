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


def generate_copyright_msg():
    """
    Generates copytight message
    :return: string containing the copyright message
    """

    copyright_str = """Copyright (C) 2016 - 2017 Karl Janson, Siavoosh Payandeh Azad, Behrad Niazmand

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>."""

    return copyright_str + '\n'


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


def gen_multi_line_comment(string):
    """
    Tunrs a string into a multi-line comment
    :param string: String to process
    :return: The multi-line comment
    """

    string = string.splitlines()

    max_line_length = 0

    # Find the maximum line length of the string
    for line in string:
        line_length = len(line)

        if line_length > max_line_length:
            max_line_length = line_length

    # Build the comment string
    comment_str = (max_line_length + 6) * '-' + '\n'

    for line in string:
        # Decode special symbols
        line = line.replace('%%-%%', max_line_length * '-')

        # Actually generate the line
        comment_str += '-- ' + line + (max_line_length - len(line) + 1) * ' ' + '--\n'

    comment_str += + (max_line_length + 6) * '-' + '\n'

    return comment_str


def generate_file_header(file_descr, noc_size):
    """
    Generates VHDL file header
    :param file_descr:  Generated file description
    :param noc_size:    Size of the network
    :return: String containing the VHDL file header for the network
    """

    header_str = file_descr + '\n%%-%%\n\n'
    header_str += generate_copyright_msg()
    header_str += '\n%%-%%\n'
    header_str += 'This file has been automatically generated. Just for you :)\n'
    header_str += 'Generated network size: ' + str(noc_size) + 'x' + str(noc_size) + '\n'

    header_str = header_str

    libraries = '\nlibrary ieee;\n'
    libraries += 'use ieee.std_logic_1164.all;\n'
    libraries += 'use IEEE.STD_LOGIC_ARITH.ALL;\n'
    libraries += 'use IEEE.STD_LOGIC_UNSIGNED.ALL;\n'
    libraries += 'USE ieee.numeric_std.ALL;\n\n'

    return gen_multi_line_comment(header_str) + libraries


def generate_file_entity(entity_name, generic, port):
    """
    Generates an VHDL entity
    :param entity_name: Name of the entity
    :param generic:     List of generics
    :param port:        List of port signals
    :return:
    """

    entity = 'entity ' + entity_name + ' is\n'
    entity += '\tgeneric(' + '<generic_placeholder>' + ');\n'
    entity += '\tport(' + '<port_placeholder>' + ');\n'
    entity += 'end ' + entity_name + ';\n\n'

    return entity


def generate_file_arch(arch_name, noc_size, component_list):
    """
    Generates Architecture part of a VHDL file
    :param arch_name: Name of the architecture
    :param noc_size: Size of the NoC
    :param component_list: List containing Component objects
    :return: A string containing the VHDL architecture
    """
    arch_contents = 'architecture behavior of ' + arch_name + ' is\n\n'
    arch_contents += generate_signal_list(component_list)
    arch_contents += '\t' + build_components(component_list, noc_size) + '\n'
    arch_contents += 'begin\n'
    arch_contents += '\t<code_placeholder>\n'
    arch_contents += 'end ' + arch_name + ';\n'

    return arch_contents


def generate_signal_list(component_list):

    signal_list_str = gen_multi_line_comment(' Signal declarations\n')
    signal_list_str +='<signal_decl_placeholder>\n'
    # for component in component_list:
    #     signal_list_str += component.

    return signal_list_str

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

    # Router instantiation
    components_str = '\n-- Router\n'
    components_str += gen_component_decl(0, noc_size, component_list['router'])

    # NI_PE instantiation
    components_str += '\n-- NI / PE\n'
    components_str += gen_component_decl(0, noc_size, component_list['ni_pe'])

    return components_str

