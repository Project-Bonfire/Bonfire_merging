"""
Parses VHDL files in order to extract the relevant parts for NW and TB generation

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

from antlr4 import *
from Scripts.include.parser.vhdl.vhdlLexer import vhdlLexer
from Scripts.include.parser.vhdl.vhdlParser import vhdlParser
from Scripts.include.antlr.vhdl_convert_listener import VHDLConvertListener
from Scripts.include.misc.helper_func import *
from Scripts.include.misc.package import *


def parse_vhd_file(vhd_file):

    # Read the input file
    input_file = FileStream(vhd_file)

    print_msg(MSG_BLUE_INFO, 'Parsing ' + vhd_file)
    # Build a lexer
    lexer = vhdlLexer(input_file)

    # Run Lexer on the file to generate the token string
    stream = CommonTokenStream(lexer)

    # Parse the token stream
    parser = vhdlParser(stream)

    # Create a parse tree wit the entire file as root node
    tree = parser.design_file()

    # Walk the tree in order to parse the CSV file
    listener = VHDLConvertListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)


def parse_vhdl(config):

    # We assume the last file in the list to be the top module for the unit
    routers_top_module = os.path.join(ROUTER_RTL_DIR, config['router'][-1])
    ni_pe_top_module = config['ni_pe'][-1]
    if 'packet_injector' in config:
        packet_injector_top_module = config['packet_injector'][-1]

    print(parse_vhd_file(routers_top_module))

