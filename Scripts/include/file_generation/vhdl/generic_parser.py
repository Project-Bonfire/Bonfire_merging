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

from Scripts.include.file_generation.vhdl.general_functions import *

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
    noc_size_x=lambda name, node_id, network_size: network_size,

    # Fault managements
    shmu_address=lambda name, node_id, network_size: name,
    self_diagnosis_address=lambda name, node_id, network_size: name,
    reconfiguration_address=lambda name, node_id, network_size: name,
    healthy_counter_threshold=lambda name, node_id, network_size: name,
    faulty_counter_threshold=lambda name, node_id, network_size: name,
    counter_depth=lambda name, node_id, network_size: name,

    # NI connection
    reserved_address=lambda name, node_id, network_size: name,
    flag_address=lambda name, node_id, network_size: name,
    counter_address=lambda name, node_id, network_size: name,
    current_x=current_x_calculator,
    current_y=current_y_calculator,
    ni_depth=lambda name, node_id, network_size: 32,  # TODO: Make it parameterizable
    ni_counter_size=lambda name, node_id, network_size: 5,  # TODO: It should be log2 if ni_depth

    # Router configuration
    rxy_rst=lambda name, node_id, network_size: 10,  # TODO: CHANGING ROUTING BITS IS NOT IMPLEMENTED
    cx_rst=cx_rst_calculator
)
