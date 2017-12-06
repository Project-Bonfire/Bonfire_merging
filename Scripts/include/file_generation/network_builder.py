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


# def get_component_parts(component):
#     inst = component.get_inst(2, 4)
#     signals = component.get_signals()
#     port_map = component.get_port_map()
#     print(signals)

def process_components(components, noc_size):
    node_count = noc_size * noc_size

    router = components['router']
    inter_component_signals = dict()

    router_port_signals = router.get_port()

    # Extract parameters for basic inter-node router signals
    for signal in router_port_signals:

        if signal['name'][:-2] == 'rx' and 'data' not in inter_component_signals:
            inter_component_signals['data'] = deepcopy(signal)

        elif signal['name'][:-2] == 'credit_out' and 'credit' not in inter_component_signals:
            inter_component_signals['credit'] = deepcopy(signal)

        elif signal['name'][:-2] == 'valid_in' and 'valid' not in inter_component_signals:
            inter_component_signals['valid'] = deepcopy(signal)

    print(inter_component_signals)
    signal_list = list()

    # for node_num, node in enumerate(range(node_count)):
    #     port_signals = router.get_port()
    #
    #     router_sig_list = list()
    #
    #     for signal in port_signals:
    #         signal_tmp = deepcopy(signal)
    #         signal_tmp['name'] = 'R_' + str(node_num) + '_' + signal_tmp['name']
    #
    #         router_sig_list.append(signal_tmp)
    #
    #     signal_list.append(router_sig_list)

    # print(signal_list)


def build_network(components, output_dir, args, logging):
    signal_list = list()
    instant_list = list()
    port_map_list = list()

    vhdl_parts = dict()

    process_components(components, 3)

    # get_component_parts(components['router'])
    vhdl_parts['header'] = generate_file_header('Project Bonfire Network File', 2)
    vhdl_parts['entity'] = generate_file_entity('network', None, None)
    vhdl_parts['arch'] = generate_file_arch('network', 2, components)  # TODO: Implement actual network size reading

    vhd_file_contents = vhdl_parts['header'] + vhdl_parts['entity'] + vhdl_parts['arch']

    # Save the file
    with open(output_dir + '/network.vhd', 'w') as vhd_file:
        vhd_file.write(vhd_file_contents)

