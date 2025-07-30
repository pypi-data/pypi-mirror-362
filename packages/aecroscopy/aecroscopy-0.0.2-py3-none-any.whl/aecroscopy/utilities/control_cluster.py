class ControlCluster:
    def __init__(self, vi_ref):
        self.vi_ref = vi_ref
        self.names = {'initialize_AR18_control_cluster': ['do_initialize_AR18'],
                      'move_tip_control_cluster': ['next_x_pos_00', 'next_y_pos_01',
                                                   'transit_time_s_02', 'do_move_tip_03'],
                      'set_setpoint_control_cluster': ['set_point_V_00',
                                                       'do_set_setpoint_01'],
                      'IO_control_cluster': ['AFM_platform_00', 'DAQ_card_01',
                                             'IO_rate_02', 'analog_input_range_03',
                                             'analog_output_range_04',
                                             'analog_output_routing_05',
                                             'analog_output_amplifier_06',
                                             'channel_01_type_07',
                                             'channel_02_type_08',
                                             'channel_03_type_09',
                                             'IO_trigger_ring_10',
                                             'do_set_IO_11'],
                      'IO_indicator_cluster': ['IO_AFM_platform_00', 'IO_card_01',
                                               'IO_rate_02', 'IO_AO_range_03',
                                               'Analog_output_routing_04',
                                               'IO_AI_range_05',
                                               'analog_output_amplifier_06',
                                               'IO_channel_011_type_07',
                                               'IO_channel_012_type_08',
                                               'IO_channel_013_type_09',
                                               'IO_trigger_ring_10']
                      }

    def get_values(self, cluster_name):
        """
        :param
            cluster_name: str
                Name of the cluster to query
        :return:
            out: dictionary
                Returns a dictionary with all of the names of parameters in the chosen cluster and their current values
        """
        out = {}
        values = self.vi_ref.getcontrolvalue(cluster_name)
        names = self.names[cluster_name]
        for name, value in zip(names, values):
            out[name] = value
        return out

    def set_values(self, cluster_name, to_write):
        """

        :param
            cluster_name: str
                Name of the cluster to write new values
        :param
            to_write: List or dictionary
                The values to be written can be provided in three ways:
                a) List: list of the all the values of the parameter in a given cluster. Raises an error if the
                    datatype of a particular value do not match with the expected datatype.
                b) Dict: dictionary of all the names from the chosen cluster and their corresponding values.
                    Checks if all the names and the datatypes match
                c) Dict: dictionary containing only a subset of parameter names and their values
                    Checks if the given names exist and the datatypes match. Only writes the provided values to the
                    cluster.
        :return:
            None
        """
        old_names, old_values = self.get_values(cluster_name).keys(), list(self.get_values(cluster_name).values())
        if isinstance(to_write, list):
            # case-1: where the values are provided as a list
            values = to_write
            self._check_dtype(values, old_values, old_names, cluster_name)
            new_values = to_write.copy()

        elif isinstance(to_write, dict):
            # case-2: where the values and names are provided in the form of a dictionary
            names, values = to_write.keys(), to_write.values()
            self._check_names(names, old_names, cluster_name)
            new_values = []
            for i, name in enumerate(old_names):
                if name in names:
                    new_values.extend([to_write[name]])
                else:
                    new_values.extend([old_values[i]])
            self._check_dtype(new_values, old_values, old_names, cluster_name)

        else:
            raise TypeError('Expected a dict or a list type for the "to_write" parameter '
                            'but received {}'.format(type(to_write)))

        self.vi_ref.setcontrolvalue(cluster_name, new_values)

    def _check_dtype(self, values, old_values,
                     old_names, cluster_name):
        for i, (value, old_value) in enumerate(zip(values, old_values)):
            if not isinstance(value, type(old_value)):
                raise TypeError('The datatype expected for {} in the {} cluster is {} '
                                'but received()'.format(type(old_values[i]), old_names[i], cluster_name,
                                                        type(values[i])))

    def _check_names(self, names, old_names, cluster_name):
        for name in names:
            if not name in old_names:
                raise KeyError('The provide name "{}" is not part of the cluster: "{}"'.format(name, cluster_name))