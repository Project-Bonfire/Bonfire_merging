"""
Implements generic VHD file generation functions

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

CLK_RST_SIG_NAMES = ['clk', 'reset', 'clock', 'rst']


def process_lines_into_string(lines, prefix='', suffix='\n', grouping_symbol=', ', group_size=1):
    """
    Changes an list of strings into a joined string, optionally adding suffices and prefixes to each line
    :param lines:           List of lines to be processed
    :param prefix:          Prefix to add to each line
    :param suffix:          Suffix to be added to each line
    :param grouping_symbol: Symbol to be used for grouping
    :param group_size:      Size of the one group (grouping_symbol is used between groups,
                            newline is injected in the end of the group)
    :return:                String containing all the substrings specified in the list
    """

    # Group lines into groups specified by group_size
    grouped_lines = [lines[i:(i + group_size)] for i in range(0, len(lines), group_size)]

    signal_declarations = list()

    for line_group in grouped_lines:
        signal_declarations.append(prefix + grouping_symbol.join(line_group) + suffix)

    lines_str = ''.join(signal_declarations) + '\n'

    return lines_str


def cx_rst_calculator(node_id, network_size):
    """
    Calculates the connection bits for a router based on network size and node's id
    :param node_id:         Address of the node
    :param network_size:    Network size
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

