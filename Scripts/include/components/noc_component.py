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
        """
        Class to store NoC component data
        and to generate VHDL code from the data
        """
        self._name = ''
        self._port = list()
        self._generic = list()

    def set_name(self, name):
        """
        Sets component name.
        :param name: Name of the component
        :return:     None
        """
        self._name = name

    def set_port(self, port_definition):
        """
        Sets port signals for the component
        :param port_definition: List of port signals
        :return: None
        """
        self._port = port_definition

    def set_generic(self, generic_definition):
        """
        Sets generic signals for the component
        :param generic_definition: List of generic signals
        :return: None
        """
        self._generic = generic_definition

    def get_name(self):
        """
        Returns component name.
        :return:     Name of the component
        """
        return self._name

    def get_port(self):
        """
        Returns port signals for the component
        :return: List of port signals
        """
        return self._port

    def get_generic(self):
        """
        Sets generic signals for the component
        :return: List of generic signals
        """
        return self._generic


    # ===================



    def get_signals(self):
        """
        Generates VHDL code for signal declaration
        :return: String containing signal declaration
        """

        signal_str = ''
        for signal in self._port:
            signal_str += 'signal ' + signal['name'] + ' : ' + signal['type'] + ';\n'

        return signal_str

    def get_port_map(self):
        """
        Generates VHDL code for port map of the current component
        :return: String containg the port map
        """
        name = 'component'  # TODO: add real name

        # Component <entity_name> is
        pmap_str = name + ': ' + self._name + '\n\n'

        # generic map (
        #   <signal1 = > signal1>;
        #   <signal2 = > signal2>;
        #   <signal3 = > signal3>
        # );
        if self._generic:
            pmap_str += '\tgeneric map (\n'

            for i, signal in enumerate(self._generic):
                signal_str = '\t\t' + signal['name'] + ' => ' \
                              + signal['name']

                if i < len(self._generic) - 1:
                    signal_str += ',\n'
                else:
                    signal_str += '\n\t)\n\n'

                pmap_str += signal_str

        # port map (
        #   <signal1 = > signal1>;
        #   <signal2 = > signal2>;
        #   <signal3 = > signal3>
        # );
        if self._port:
            pmap_str += '\tport map (\n'

            for i, signal in enumerate(self._port):
                signal_str = '\t\t' + signal['name'] + ' => ' \
                             + signal['name']

                if i < len(self._port) - 1:
                    signal_str += ',\n'
                else:
                    signal_str += '\n\t);\n\n'

                pmap_str += signal_str

        else:
            raise RuntimeError('Tried to read port values, but they were empty. Something\'s wrong...')

        return pmap_str

