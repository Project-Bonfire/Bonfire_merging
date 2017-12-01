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

from Scripts.include.file_generation.vhdl_generation import *


# def get_component_parts(component):
#     inst = component.get_inst(2, 4)
#     signals = component.get_signals()
#     port_map = component.get_port_map()
#     print(signals)


def build_network(components, output_dir, args, logging):
    signal_list = list()
    instant_list = list()
    port_map_list = list()

    vhdl_parts = dict()

    # get_component_parts(components['router'])
    vhdl_parts['header'] = generate_file_header('Project Bonfire Network File', 4)
    vhdl_parts['entity'] = generate_file_entity('network', None, None)
    vhdl_parts['arch'] = generate_file_arch('network', 4, components)  # TODO: Implement actual network size reading

    vhdl_string = vhdl_parts['header'] + vhdl_parts['entity'] + vhdl_parts['arch']

    # Save the file
    with open(output_dir + '/network.vhd', 'w') as vhd_file:
        vhd_file.write(vhdl_string)

