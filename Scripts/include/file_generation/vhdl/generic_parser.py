"""
Defines what to do with generics in components

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


def cx_rst_calculator(_, node_id, network_size):
    """
    Calculates the connection bits for a router based on network size and node's id
    :return:                Connection bits
    """

    node_x = node_id % network_size
    node_y = node_id / network_size

    c_n = 1
    c_e = 1
    c_w = 1
    c_s = 1

    if node_y == 0:
        c_n = 0

    elif node_y == network_size - 1:
        c_s = 0

    if node_x == 0:
        c_w = 0

    elif node_x == network_size - 1:
        c_e = 0

    cx_rst = c_s * 8 + c_w * 4 + c_e * 2 + c_n

    return cx_rst


"""
Describes and action which should be done to generics when generic map is analyzed.
Keys in the dict below represent the generic names.

Each generic will be called as a function with the following parameters:
    name: name of the generic
    node_id: ID if the current node
    network_size: size of the network
    
Adding new generics:
* return a constant (or easily calculable value): use a lambda function.
* using a real function: specify the name of the function (without parameter declaration)
"""
GENERIC_DECISION_LIST = dict(
    # General network_component parameters
    current_address=lambda name, node_id, network_size: node_id,
    noc_size=lambda name, node_id, network_size: name,
    data_width=lambda name, node_id, network_size: name,

    # Fault managements
    shmu_address=lambda name, node_id, network_size: name,
    self_diagnosis_address=lambda name, node_id, network_size: name,
    reconfiguration_address=lambda name, node_id, network_size: name,
    healthy_counter_threshold=lambda name, node_id, network_size: name,
    faulty_counter_threshold=lambda name, node_id, network_size: name,
    counter_depth=lambda name, node_id, network_size: name,

    # Noc connection
    reserved_address=lambda name, node_id, network_size: name,
    flag_address=lambda name, node_id, network_size: name,
    counter_address=lambda name, node_id, network_size: name,

    # Router configuration
    rxy_rst=lambda name, node_id, network_size: 10,  # TODO: CHANGING ROUTING BITS IS NOT IMPLEMENTED
    cx_rst=cx_rst_calculator
)
