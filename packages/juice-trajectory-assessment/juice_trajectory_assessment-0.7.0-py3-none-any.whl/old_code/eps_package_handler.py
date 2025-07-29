"""
Created on July, 2020

@author: Claudio Munoz Crego (ESAC)

This Module allows to handle EPS Package from Juice Timeline Tool,
running eps if needed using eps wrapper

"""

from esac_juice_pyutils.commons import json_handler as my_json
import old_code.soa_run_eps as soa_run_eps


class EpsPackageHandler(object):
    """
    This Class allows handle EPS Package from Juice Timeline Tool
    """

    def __init__(self, output_dir="./"):

        self.output_dir = output_dir

        self.simu = None
        self.eps_param = None

    def set_up_from_parameters(self, json_data, experiment_types=['target']):
        """
        Set up from parameters
        and un EPS if requested

        :param json_data: dico json like
        :param experiment_types: list of EPS experiment types (target, instrument, WG)
        """

        from collections import namedtuple

        m = json_data["requests"]
        self.simu = namedtuple('Struct', m.keys())(*m.values())

        if 'soa_eps' in json_data:
            o = json_data["soa_eps"]
            self.eps_param = namedtuple('Struct', o.keys())(*o.values())

            for experiment_type in experiment_types:
                soa_run_eps.run(self.simu.root_path, self.simu.scenario, experiment_type, self.eps_param)

    def set_up_from_json_file(self, json_file, experiment_types=['target']):
        """
        Set up  from json config files
        and un EPS if requested

        :param json_file: configuration file
        :param experiment_types: list of EPS experiment types (target, instrument, WG)
        :return:
        """

        x = my_json.load_to_object(json_file)

        self.simu = x.requests

        if hasattr(x, 'soa_eps'):
            self.eps_param = x.soa_eps

            for experiment_type in experiment_types:
                soa_run_eps.run(self.simu.root_path, self.simu.scenario, experiment_type, self.eps_param)
