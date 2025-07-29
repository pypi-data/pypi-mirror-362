"""
Created on July, 2019

@author: Claudio Munoz Crego (ESAC)

This Module allows to handle (parse, load) mission phase files
"""

import logging
import os

import sys
import pandas as pd
import datetime

from juice_trajectory_assessment.commons.mission_phases_handler import MissionPhaseHandler

if __name__ == '__main__':

    from esac_juice_pyutils.commons.my_log import setup_logger

    here = os.path.abspath(os.path.dirname(__file__))
    test_dir = os.path.dirname(here)

    print(here)
    print(test_dir)

    setup_logger('debug')
    print(os.getcwd())

    print('\n-----------------------------------------------\n')

    logging.debug('Start of test')

    input_file = '../test_files/conf/crema_3.2/Mission_phases.txt'

    mission_phases = MissionPhaseHandler(input_file).get_mission_phases()

    logging.debug('End of test')
