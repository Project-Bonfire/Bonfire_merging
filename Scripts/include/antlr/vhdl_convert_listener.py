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

import antlr4
from Scripts.include.parser.vhdl.vhdlListener import vhdlListener
from Scripts.include.parser.vhdl.vhdlParser import vhdlParser


class VHDLConvertListener(vhdlListener):

    def __init__(self):
        self._processing_entity = False
        self._processing_generic = False
        self._processing_port = False
        self._processing_identifier_list = False

        self._port_declarations = list()
        self._generic_declarations = list()

        self._line_temp = dict()

    # def enterIdentifier(self, ctx:vhdlParser.IdentifierContext):
    #     print('identifier', ctx.getText())

    def enterEntity_header(self, ctx:vhdlParser.Entity_headerContext):
        """
        Sets a flag that we are processing the header
        :param ctx: current context
        :return: None
        """
        self._processing_entity = True
        # print('entity', ctx.getText())

    def exitEntity_header(self, ctx:vhdlParser.Entity_headerContext):
        """
        Resets a flag that we are processing the header
        :param ctx: current context
        :return: None
        """
        self._processing_entity = False

    def enterInterface_constant_declaration(self, ctx:vhdlParser.Interface_constant_declarationContext):
        """
        Sets a flag that we are processing the generics declaration
        :param ctx: current context
        :return: None
        """
        if self._processing_entity:
            self._processing_generic = True

    def exitInterface_constant_declaration(self, ctx:vhdlParser.Interface_constant_declarationContext):
        """
        Sets a flag that we are processing the generics declaration
        :param ctx: current context
        :return: None
        """
        if self._processing_entity:
            self._processing_generic = False

    def enterInterface_port_declaration(self, ctx:vhdlParser.Interface_constant_declarationContext):
        """
        Sets a flag that we are processing the port declaration
        :param ctx: current context
        :return: None
        """
        if self._processing_entity:
            self._processing_port = True

    def exitInterface_port_declaration(self, ctx:vhdlParser.Interface_constant_declarationContext):
        """
        Resets a flag that we are processing the port declaration
        :param ctx: current context
        :return: None
        """
        if self._processing_entity:
            self._processing_port = False

    def enterIdentifier_list(self, ctx:vhdlParser.Identifier_listContext):
        """
        Sets a flag that we are processing the identifier list
        :param ctx: current context
        :return: None
        """
        if self._processing_entity:
            self._processing_identifier_list = True

    def exitIdentifier_list(self, ctx:vhdlParser.Identifier_listContext):
        """
        Resets a flag that we are processing the identifier list
        :param ctx: current context
        :return: None
        """
        if self._processing_entity:
            self._processing_identifier_list = False

    def enterIdentifier(self, ctx:vhdlParser.IdentifierContext):
        if self._processing_entity:
            print(ctx.getText())
