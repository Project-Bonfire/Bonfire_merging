"""
Implements entity generation functions for VHDL files

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


def generate_entity(conn_if, ident_level, design_generation):

    port_signal_list_str = 'clk : in std_logic;\n'
    port_signal_list_str += ident(ident_level) + 'reset : in std_logic'

    port_signal_list = list()

    for connection_type, conn in sorted(conn_if.items()):
        if 'general_' in connection_type:
            for signal in conn.values():
                if signal['name'] not in CLK_RST_SIG_NAMES:
                    signal_string = signal['name'] + ': ' + signal['direction'] + ' ' + signal['type']
                    port_signal_list.append(signal_string)
    port_signal_list_str += process_lines_into_string(sorted(port_signal_list),
                                                      prefix=';\n' + ident(ident_level),
                                                      suffix='')
    return port_signal_list_str
