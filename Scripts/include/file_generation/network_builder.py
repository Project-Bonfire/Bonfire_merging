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


def get_component_parts(component):
    inst = component.get_inst()
    signals = component.get_signals()
    port_map = component.get_port_map()
    print(port_map)


def build_network(components, output_dir, args, logging):
    signal_list = list()
    instant_list = list()
    port_map_list = list()

    get_component_parts(components['router'])
