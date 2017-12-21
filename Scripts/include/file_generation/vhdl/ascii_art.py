"""
Implements generic VHD file generation functions

Copyright (C) 2016 - 2017 Siavoosh Payandeh Azad, Karl Janson, Behrad Niazmand

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


class ASCIIBuffer:
    def __init__(self):
        self._buf = list()

        self._current_line = ''

    def newline(self):
        self._buf.append(self._current_line)
        self._current_line = ''

    def write(self, string):
        self._current_line = self._current_line + string

    def writeln(self, string):
        self._current_line = self._current_line + string
        self._buf.append(self._current_line)
        self._current_line = ''

    def get_contents(self):
        return self._buf


def generate_ascii_art(noc_size):

    art_buffer = ASCIIBuffer()

    art_buffer.writeln("--     X --------------->")

    for y_axis in range(noc_size):

        # Draw Y axis line
        if y_axis == 0:
            art_buffer.write("--  Y ")

        else:
            art_buffer.write("--  | ")

        # Draw horizontal node borders
        for x_axis in range(noc_size):
            art_buffer.write("       ----")

        art_buffer.newline()
        art_buffer.write("--  |      ")

        for x_axis in range(noc_size):
            if x_axis != noc_size - 1:
                link = "---"

                if (x_axis + noc_size * y_axis) >= 10:
                    art_buffer.write(" |" + str(x_axis + noc_size * y_axis) + " | " + link)
                else:
                    art_buffer.write(" | " + str(x_axis + noc_size * y_axis) + "  | " + link)
            else:
                if (x_axis + noc_size * y_axis) >= 10:
                    art_buffer.write(" | " + str(x_axis + noc_size * y_axis) + " |")
                else:
                    art_buffer.write(" | " + str(x_axis + noc_size * y_axis) + "  |")

        art_buffer.newline()
        link = "|"

        if y_axis == noc_size - 1:
            art_buffer.write("--  v ")
        else:
            art_buffer.write("--  | ")

        for x_axis in range(0, noc_size):
            art_buffer.write("       ----")

        if y_axis == noc_size - 1:
            art_buffer.newline()
            for x_axis in range(0, noc_size):
                art_buffer.write("           ")
        else:
            art_buffer.newline()
            art_buffer.write("--  |")
            for x_axis in range(0, noc_size):
                art_buffer.write("          " + link)

        art_buffer.newline()

    title = gen_multi_line_comment('Organization of the Network')
    art_str = process_lines_into_string(art_buffer.get_contents())

    return title + '\n' + art_str
