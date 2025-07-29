"""
Created on July, 2020

@author: Claudio Munoz Crego (ESAC)

This Module allows to test TrajAssessmentFilter
"""

import logging


def test_0(start, end):

    root_path_input = '../TDS/JIRA_TEST/JSA-286'
    mission_phase = '../test_files/conf/crema_3.0/Mission_phases.txt'
    trajectory_input_file = 'trajectory_metrics_data_3_0.csv'
    trajectory_input_path = os.path.join(root_path_input, trajectory_input_file)
    coverage_input_file = 'coverage_inputs_n54_pp5_q19_v02.json'
    coverage_input_path = os.path.join(root_path_input, coverage_input_file)
    eps_package = 'eps_package'
    eps_package_input_path = os.path.join(eps_package)
    output_dir = './'

    eps_package_param = {
        "requests":
            {
                "root_path": "../TDS/JIRA_TEST/JSA-286",
                "scenario": "eps_package",
            },
        "soa_eps": {
            "path_eps_pwr": "../TDS/conf/MAPPS/CONFIG/SIMULATION_DATA/dummy.pwr",
            "path_eps_brf": "$HOME/python3/soa_report/test_files/MAPPS/CONFIG/SIMULATION_DATA/juice_0.0.4.brf",
            "epsng": "/Users/cmunoz/JUICE_SO/SOFTWARE/EPS/bin_mac/eps",
            "epscfg": "../TDS/conf/MAPPS/CONFIG/CONFIG_DATA/eps_juice.cfg",
            "epsdata": "../TDS/conf/MAPPS/CONFIG/CONFIG_DATA",
            "evf_data": "../TDS/JIRA_TEST/JSA-286/eps_package/target/TOP_events.evf",
            "itl_data": "../TDS/JIRA_TEST/JSA-286/eps_package/target/ITL/TOP_timelines.itl",
            "edf_data": "../TDS/JIRA_TEST/JSA-286/eps_package/target/EDF/TOP_experiments.edf",
            "report_time_step": 600,
            "simu_time_step": 60
        },
        "request_parameter_descriptions": {
            "root_path": "path of directory where eps_package is located ",
            "scenario": "Name of the eps_package (directory)"
        },
        "soa_eps_descriptions": {
            "path_eps_pwr": "path of pwr file",
            "path_eps_brf": "path of datarate file",
            "epsng": "path of eps tool (executable running in current OS)",
            "epscfg": "path of cfg file; default is <EPS_CONGIF_DATA>/eps.cfg",
            "epsdata": "path of eps data and configuration file",
            "report_time_step": "Defines the eps output reporting time step  (default: 60 seconds)",
            "simu_time_step": "Defines the simulation delta time step (default: 1 seconds)"
        }
    }

    p = TrajAssessmentFilter(start, end, mission_phase, output_dir=output_dir)
    p.create_report(trajectory_input_path, coverage_input_path, eps_package_param, output_dir)


def test_01(start, end):

    root_path_input = '../TDS/JIRA_TEST/JSA-295/input'
    mission_phase = '../test_files/conf/crema_3.0/Mission_phases.txt'
    trajectory_input_file = 'trajectory_metrics_data_3_0.csv'
    trajectory_input_path = os.path.join(root_path_input, trajectory_input_file)
    coverage_input_file = 'coverage_inputs_n54_pp5_q19_v02.json'
    coverage_input_path = os.path.join(root_path_input, coverage_input_file)
    eps_package = 'eps_package'
    eps_package_input_path = os.path.join(eps_package)
    output_dir = './'

    eps_package_param = {
        "requests":
            {
                "root_path": "../TDS/JIRA_TEST/JSA-295/input",
                "scenario": "eps_package",
            },
        "soa_eps": {
            "path_eps_pwr": "../TDS/conf/MAPPS/CONFIG/SIMULATION_DATA/dummy.pwr",
            "path_eps_brf": "../TDS/conf/MAPPS/CONFIG/juice_0.0.4.brf",
            "epsng": "/Users/cmunoz/JUICE_SO/SOFTWARE/EPS/bin_mac/eps",
            "epscfg": "../TDS/conf/MAPPS/CONFIG/CONFIG_DATA/eps_juice.cfg",
            "epsdata": "../TDS/conf/MAPPS/CONFIG/CONFIG_DATA",
            "evf_data": "../TDS/JIRA_TEST/JSA-295/input/eps_package/target/TOP_events.evf",
            "itl_data": "../TDS/JIRA_TEST/JSA-295/input/eps_package/target/ITL/TOP_timelines.itl",
            "edf_data": "../TDS/JIRA_TEST/JSA-295/input/eps_package/target/EDF/TOP_experiments.edf",
            "report_time_step": 600,
            "simu_time_step": 60
        },
        "request_parameter_descriptions": {
            "root_path": "path of directory where eps_package is located ",
            "scenario": "Name of the eps_package (directory)"
        },
        "soa_eps_descriptions": {
            "path_eps_pwr": "path of pwr file",
            "path_eps_brf": "path of datarate file",
            "epsng": "path of eps tool (executable running in current OS)",
            "epscfg": "path of cfg file; default is <EPS_CONGIF_DATA>/eps.cfg",
            "epsdata": "path of eps data and configuration file",
            "report_time_step": "Defines the eps output reporting time step  (default: 60 seconds)",
            "simu_time_step": "Defines the simulation delta time step (default: 1 seconds)"
        }
    }

    p = TrajAssessmentFilter(start, end, mission_phase, output_dir=output_dir)
    p.create_report(trajectory_input_path, coverage_input_path, eps_package_param, output_dir)


def test_1(start, end):

    from esac_juice_pyutils.commons import json_handler as my_json

    here = os.path.abspath(os.path.dirname(__file__))

    cfg_file = "../TDS/JIRA_TEST/JSA-295/traj_assessment_report_jsa_295.json"

    test_dir = os.path.dirname(cfg_file)
    cfg = my_json.load_to_dic(cfg_file)

    os.chdir(test_dir)

    cfg_main = cfg['main']

    root_path = cfg_main['root_path']
    logging.info('goto root test directory: {}'.format(root_path))

    root_path_input = os.path.join(root_path, cfg_main['input'])
    mission_phase = cfg_main['mission_phase']
    trajectory_input_file = cfg_main['trajectory_input_file']
    trajectory_input_path = os.path.join(root_path_input, trajectory_input_file)
    coverage_input_file = cfg_main['coverage_input_file']
    coverage_input_path = os.path.join(root_path_input, coverage_input_file)

    output_dir = cfg_main['output_dir']

    eps_package_param = cfg['eps_package_param']

    p = TrajAssessmentFilter(start, end, mission_phase, output_dir=output_dir)
    p.create_report(trajectory_input_path, coverage_input_path, eps_package_param, output_dir)

    os.chdir(here)
    logging.debug('goto root original directory: {}'.format(here))


if __name__ == '__main__':

    import os
    from esac_juice_pyutils.commons import tds
    from esac_juice_pyutils.commons.my_log import setup_logger
    from juice_trajectory_assessment.report.traj_assessment_report import TrajAssessmentFilter

    test_dir = os.path.abspath(os.path.dirname(__file__))
    project_dir = os.path.dirname(test_dir)

    setup_logger('info')
    print('local directory = ', os.getcwd())

    print('\n-----------------------------------------------\n')
    logging.debug('start test')

    Start_time = '2030-09-28T02:16:00'
    End_time = '2030-10-27T04:06:35'

    start = tds.str2datetime(Start_time)
    end = tds.str2datetime(End_time)

    test_1(start, end)

    logging.debug('end of test')
