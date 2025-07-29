"""
Created on May 2023

@author: Claudio Munoz Crego (ESAC)

This Module allows run the Trajectory assessment reporter for several cases

All the data are available on test_data_set directory

1) Generate trajectory reporter for crema_5_1_150lb_23_1
The result is compared against a previous run (here the rst report)

2) Regenerate the report without running simulation and including the cruise information.
"""

import os
import logging
import unittest

from esac_juice_pyutils.commons.json_handler import load_to_dic
from juice_trajectory_assessment.trajectory_assessment_report_cmd import set_parameters
from juice_trajectory_assessment.report.traj_assessment_report import TrajAssessmentFilter

test_data_set = '../TDS/crema_5_1_150lb_23_1'

# disable logging during unit test
logging.disable(logging.CRITICAL)


class MyTestCase(unittest.TestCase):

    maxDiff = None

    def test_trajectory_report(self,):
        """
        Test (case 1) check trajectory report generated as expected
        """

        here = os.getcwd()
        print(here)
        os.chdir(test_data_set)
        working_dir = os.getcwd()

        config_file = 'traj_assessment_report_5_1_150lb_23_1.json'

        cfg_file = load_to_dic(config_file)
        output_ref = cfg_file['main']["output_dir"]

        env_var, report_title, report_name, run_simu = set_parameters(cfg_file)
        report_name_tmp = report_name + '_tmp'

        start = end = None  # not needed at least for now
        p = TrajAssessmentFilter(start, end, env_var, output_dir=output_ref)
        p.set_crema_ref('id', cfg_file, run_simu=run_simu)
        p.create_report(working_dir, output_ref,
                        report_title=report_title,
                        objective='',
                        new_report_name=report_name_tmp)

        tmp_values = list(open(os.path.join(output_ref, f'{report_name_tmp}.rst'), 'r'))
        tmp_ref = list(open(os.path.join(output_ref, f'{report_name}_ref.rst'), 'r'))

        self.assertListEqual(tmp_values, tmp_ref)

        for f_tmp in os.listdir():
            if report_name_tmp in f_tmp:
                os.remove(f_tmp)

        os.chdir(here)