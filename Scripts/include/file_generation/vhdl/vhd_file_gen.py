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

from Scripts.include.file_generation.vhdl.generic_functions import *
from Scripts.include.file_generation.vhdl import vhd_header_gen
from Scripts.include.file_generation.vhdl import vhd_arch_gen


def generate_file_header(file_descr, noc_size):
    """
    Generates VHDL file header
    :param file_descr:  Generated file description
    :param noc_size:    Size of the network
    :return: String containing the VHDL file header for the network
    """

    header_str = file_descr + '\n%%-%%\n\n'
    header_str += vhd_header_gen.generate_copyright_msg()
    header_str += '%%-%%\n'
    header_str += 'This file has been automatically generated. Just for you :)\n'
    header_str += 'Generated network size: ' + str(noc_size) + 'x' + str(noc_size) + '\n'

    libraries = vhd_header_gen.gen_library_include()

    vhd_header = gen_multi_line_comment(header_str) + '\n' + libraries

    return vhd_header


# TODO: IMPLEMENT ENTITY GENERATION
def generate_file_entity(entity_name, generic, port):

    entity = 'entity ' + entity_name + ' is\n'
    entity += '\tgeneric(' + '<generic_placeholder>' + ');\n'
    entity += '\tport(' + '<port_placeholder>' + ');\n'
    entity += 'end ' + entity_name + ';\n\n'

    return entity


def generate_file_arch(arch_name, noc_size, component_list, conn_if):
    """
    Generates Architecture part of a VHDL file
    :param arch_name: Name of the architecture
    :param noc_size: Size of the NoC
    :param component_list: List containing Component objects
    :param conn_if: Signals for connecting the components together
    :return: A string containing the VHDL architecture
    """

    node_count = noc_size * noc_size

    signal_list = vhd_arch_gen.generate_signal_list(conn_if, node_count)
    component_decl = vhd_arch_gen.build_components(component_list, noc_size)
    port_maps = vhd_arch_gen.generate_port_maps(component_list, node_count)

    arch_contents = 'architecture behavior of ' + arch_name + ' is\n\n'
    arch_contents += signal_list
    arch_contents += '\t' + component_decl + '\n'
    arch_contents += 'begin\n'
    arch_contents += port_maps + '\n'
    arch_contents += 'end ' + arch_name + ';\n'

    return arch_contents
