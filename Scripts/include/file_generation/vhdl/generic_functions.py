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


def process_lines_into_string(lines, prefix='', suffix='\n', grouping_symbol=', ',
                              group_size=1, block_end_newline=False):
    """
    Changes an list of strings into a joined string, optionally adding suffices and prefixes to each line
    :param lines:               List of lines to be processed
    :param prefix:              Prefix to add to each line
    :param suffix:              Suffix to be added to each line
    :param grouping_symbol:     Symbol to be used for grouping
    :param group_size:          Size of the one group (grouping_symbol is used between groups,
                                    newline is injected in the end of the group)
    :param block_end_newline:   Character to put in the end of the entire block
    :return:                    String containing all the substrings specified in the list
    """

    # Group lines into groups specified by group_size
    grouped_lines = [lines[i:(i + group_size)] for i in range(0, len(lines), group_size)]

    group_elements = list()

    for line_group in grouped_lines:
        group_elements.append(prefix + grouping_symbol.join(line_group) + suffix)

    lines_str = ''.join(group_elements) + ('\n' if block_end_newline else '')

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


def gen_multi_line_comment(string, comment_char='-'):
    """
    Tunrs a string into a multi-line comment
    :param string: String to process
    :param comment_char: Character to be used for comments
    :return: The multi-line comment
    """

    string = string.splitlines()

    # Find the maximum line length of the string
    max_line_length = max([[len(line)] for line in string])[0]

    # Build the comment
    comment_lines = [(max_line_length + 6) * comment_char]

    for line in string:

        # Decode special symbols
        line = line.replace('%%-%%', max_line_length * comment_char)

        line_prefix = 2 * comment_char + ' '
        line_suffix = (max_line_length - len(line) + 1) * ' ' + 2 * comment_char

        comment_lines.append(line_prefix + line + line_suffix)

    comment_lines.append((max_line_length + 6) * comment_char)

    # Actually build the string
    comment_str = process_lines_into_string(comment_lines)

    return comment_str


def ident(ident_level):
    """
    Returns the number of tabs specified in the 'ident_level' parameter
    :param ident_level: how many tabs to insert
    :return:
    """
    return ident_level * '\t'
