"""
Generic NoC component class

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


class NoCComponent(object):

    def __init__(self):
        self._name = ''
        self._port = list()
        self._generic = list()

    def set_name(self, name):
        self._name = name

    def set_port(self, port_definition):
        self._port = port_definition

    def set_generic(self, generic_definition):
        self._generic = generic_definition


