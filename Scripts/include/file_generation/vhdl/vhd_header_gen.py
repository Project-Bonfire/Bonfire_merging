"""
Implements VHD file header generation functions

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


def generate_copyright_msg():
    """
    Generates copytight message
    :return: string containing the copyright message
    """

    copyright_lines = ['Copyright (C) 2016 - 2017 Karl Janson, Siavoosh Payandeh Azad, Behrad Niazmand',
                       '',
                       'This program is free software: you can redistribute it and/or modify',
                       'it under the terms of the GNU General Public License as published by',
                       'the Free Software Foundation, either version 3 of the License, or',
                       '(at your option) any later version.',
                       '',
                       'This program is distributed in the hope that it will be useful,',
                       'but WITHOUT ANY WARRANTY; without even the implied warranty of',
                       'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the',
                       'GNU General Public License for more details.',
                       '',
                       'You should have received a copy of the GNU General Public License',
                       'along with this program.  If not, see <http://www.gnu.org/licenses/>.']

    copyright_msg = process_lines_into_string(copyright_lines)

    return copyright_msg


def gen_library_include():
    """
    Returns a string with libraries to be included in the VHD file
    :return: String containing the libraries
    """

    libraries = ['library IEEE',
                 'use IEEE.std_logic_1164.ALL',
                 'use IEEE.std_logic_arith.ALL',
                 'use IEEE.std_logic_unsigned.ALL',
                 'USE IEEE.numeric_std.ALL']

    lib_str = process_lines_into_string(libraries, suffix=';\n', block_end_newline=True)

    return lib_str
