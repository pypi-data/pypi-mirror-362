"""
Created on July, 2020

@author: Claudio Munoz Crego (ESAC)

This Module allows to handle Coverage info

"""

import os
import sys
import logging
import datetime
import pandas as pd

from esac_juice_pyutils.commons.json_handler import load_to_dic


class CoverageInfo(object):
    """
    This Class allows read and parse Coverage info file
    """

    def __init__(self, input_file, output_dir="./"):

        self.output_dir = output_dir

        self.dico = self.read(input_file)

    def read(self, input_file):
        """
        Read json info from file

        :return: coverage_info: dictionary including key, value
        """

        logging.debug('Reading file: {}'.format(input_file))

        if not os.path.exists(input_file):
            logging.error('File does not exist: {}'.format(input_file))
            sys.exit()

        else:

            dico = load_to_dic(input_file)

        return dico

    def dico2metric(self):
        """
        translate dico to key values list with header
        :return: metrics, a list of list containing metrics lists with headers in first row
        """

        metrics = [['Parameters', 'values', 'Descr']]

        for k, v in self.dico['mandatory_inputs'].items():

            descr = 'TBD'
            if k in self.dico['Descriptions'].keys():
                descr = self.dico['Descriptions'][k]

            metrics.append([k, v, descr])

        for k, v in self.dico['optional_inputs'].items():

            descr = 'TBD'
            if k in self.dico['Descriptions'].keys():
                descr = self.dico['Descriptions'][k]

            metrics.append([k, v, descr])

        return metrics

