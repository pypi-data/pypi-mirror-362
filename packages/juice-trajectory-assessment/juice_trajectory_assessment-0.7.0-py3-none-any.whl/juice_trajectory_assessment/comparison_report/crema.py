"""
Created on January 2021

@author: Claudio Munoz Crego (ESAC)

This Module allows to build a crema object including data for reporting Trajectory Assessment Comparison
"""
import os
import sys
import logging

from juice_trajectory_assessment.commons.trajectory_info_handler import TrajectoryInfo
# from old_code.eps_package_handler import EpsPackageHandler
from juice_trajectory_assessment.commons.mission_phases_handler import MissionPhaseHandler
from juice_trajectory_assessment.commons.ca_event_handler import get_radio_source_occ_per_flyby

from soa_report.juice.eps_data.data_rate_avg import DataRateAverage
from osve_wrapper.osve_advanced_wrapper import run_osve


class Crema(object):

    def __init__(self, crema_id, config, env_var=None, juice_conf=None,
                 path_to_osve_lib_dir=None, kernel=None, run_simu=True,
                 include_dv_section=True, include_cruise=False):

        self.crema_id = crema_id

        self.env_var = env_var

        self.mission_phase = None

        self.tour_start = None
        self.tour_end = None
        self.gco500_start = None
        self.gco500_end = None
        self.tour_sub_phase = None
        self.ganymede_sub_phase = None

        self.reported_period_start = None
        self.reported_period_end = None

        self.my_date_partitions = []

        self.trajectory_info = None

        self.include_dv_section = include_dv_section
        self.eps_dataframes = None
        self.run_simu = run_simu
        self.expres_dataframes = None

        self.coverage_info = None

        self.wg3_trajectory_metrics_path = None

        self.gs_plots = None

        self.other_plots = None

        self.include_cruise = include_cruise

        self.perijove_details = None
        self.flyby_details = None
        self.cruise_details = None

        self.docx_template = None

        self.set_crema(config, juice_conf=juice_conf, path_to_osve_lib_dir=path_to_osve_lib_dir, kernel=kernel)

    def set_crema(self, config, juice_conf=None, path_to_osve_lib_dir=None, kernel={}):
        """
        Set all the variable for the current crema

        :param config: crema parameters
        :param juice_conf: path of juice configuration
        :param path_to_osve_lib_dir: path of osve lib
        :param kernel: kernel parameters
        """

        if "root_path" in config.keys():
            root_path = config["root_path"]
            root_path = self.env_var.subsitute_env_vars_in_path(root_path)
        else:
            logging.error('root_path parameters must be specified in configuration file')
            sys.exit()

        if kernel == {}:
            logging.error('"kernel" not defined in configuration file')
            sys.exit()

        if 'eps_package_param' in config.keys():
            # no longer supported
            logging.warning('eps no longer supported for juice')
            sys.exit()

        if 'osve' in config.keys():

            osve_param = config['osve']

            if 'juice_conf' not in osve_param.keys():
                if juice_conf:
                    juice_conf = self.env_var.subsitute_env_vars_in_path(juice_conf)
                    osve_param['juice_conf'] = juice_conf
                else:
                    logging.error('"juice_conf" not defined in configuration file')

            if 'path_to_osve_lib_dir' not in osve_param.keys():
                if path_to_osve_lib_dir:
                    path_to_osve_lib_dir = self.env_var.subsitute_env_vars_in_path(path_to_osve_lib_dir)
                    osve_param['path_to_osve_lib_dir'] = path_to_osve_lib_dir
                else:
                    logging.error('"path_to_osve_lib_dir" not defined in configuration file')

            if self.env_var and 'path_eps_brf' in osve_param.keys():
                path_eps_brf = osve_param['path_eps_brf']
                osve_param['path_eps_brf'] = self.env_var.subsitute_env_vars_in_path(path_eps_brf)

            crema_id = osve_param["crema_id"]
            crema_id_x_y =crema_id.replace('crema_', '')

            osve_param['kernel'] = kernel
            if 'local_root_dir' in osve_param['kernel']:
                osve_param['kernel']['local_root_dir'] = \
                    self.env_var.subsitute_env_vars_in_path(osve_param['kernel']['local_root_dir'])

            geopipeline_output = os.path.join(juice_conf, 'internal', 'geopipeline', 'output', crema_id.capitalize())
            trajectory_ouput = os.path.join(geopipeline_output, 'trajectory')
            timeline_ouput = os.path.join(juice_conf, 'internal', 'timeline', 'output', crema_id)
            coverage_ouput = os.path.join(juice_conf, 'internal', 'coverage_tool', 'output', crema_id,
                                          'trajectory_assessment')

            if 'ptr' in osve_param.keys():
                osve_param['ptr'] = self.env_var.subsitute_env_vars_in_path(osve_param['ptr'])
            else:
                osve_param['ptr'] = os.path.join(timeline_ouput,
                                                 'spice_segmentation_attitude_{}.ptx'.format(str(crema_id_x_y)))

            if 'no_ptr_cut' not in osve_param.keys():
                osve_param['no_ptr_cut'] = False  # by default enforce cut PTR to the TOP_ITL start/end times

            if self.include_dv_section:

                here = os.getcwd()
                os.chdir(root_path)
                self.get_osve_data_frame(osve_param)
                os.chdir(here)

            else:

                logging.info('DV section no included')

            if "mission_phase" in config.keys():
                mission_phase_path = config["mission_phase"]
                mission_phase_path = self.env_var.subsitute_env_vars_in_path(mission_phase_path)
            else:
                mission_phase_path = os.path.join(juice_conf, 'internal', 'geopipeline', 'output', crema_id,
                                                  'Mission_Phases.csv')
            config["mission_phase"] = mission_phase_path
            logging.info('mission_phase: {}'.format(mission_phase_path))

            if "mission_timeline_flyby" in config.keys():
                mission_timeline_flyby = config["mission_timeline_flyby"]
                mission_timeline_flyby = self.env_var.subsitute_env_vars_in_path(mission_timeline_flyby)
            else:
                mission_timeline_event_file_name = 'mission_timeline_event_file_{}.csv'.format(crema_id_x_y)
                mission_timeline_flyby = os.path.join(geopipeline_output, mission_timeline_event_file_name)

            config["mission_timeline_flyby"] = mission_timeline_flyby
            logging.info('mission_timeline_flyby: {}'.format(mission_timeline_flyby))

            if 'wg3_trajectory_metrics' in config.keys():
                wg3_trajectory_metrics_path = config['wg3_trajectory_metrics']
                wg3_trajectory_metrics_path = self.env_var.subsitute_env_vars_in_path(wg3_trajectory_metrics_path)
            else:
                wg3_trajectory_metrics_path = os.path.join(trajectory_ouput, 'wg3_trajectory_metrics')

            config['wg3_trajectory_metrics'] = wg3_trajectory_metrics_path
            self.wg3_trajectory_metrics_path = wg3_trajectory_metrics_path
            logging.info('wg3_trajectory_metrics: {}'.format(wg3_trajectory_metrics_path))

            if 'trajectory_input_file' in config.keys():
                trajectory_input_path = config['trajectory_input_file']
                trajectory_input_path = self.env_var.subsitute_env_vars_in_path(trajectory_input_path)
            else:
                trajectory_input_file_name = 'trajectory_metrics_data_{}.csv'.format(crema_id_x_y)
                trajectory_input_path = os.path.join(trajectory_ouput, trajectory_input_file_name)
                trajectory_input_path = self.env_var.subsitute_env_vars_in_path(trajectory_input_path)

            config['trajectory_input_file'] = trajectory_input_path
            self.set_traj_info_metric(trajectory_input_path)

            logging.info('trajectory_input_file: {}'.format(trajectory_input_path))

            if 'coverage_input_dir' in config.keys():
                coverage_input_path = config['coverage_input_dir']
                coverage_input_path = self.env_var.subsitute_env_vars_in_path(coverage_input_path)
            else:
                coverage_input_path = coverage_ouput

            config['coverage_input_dir'] = coverage_input_path
            logging.info('coverage_input_dir: {}'.format(coverage_input_path))

            if 'ground_station_plots' in config.keys():
                gs_plots = config['ground_station_plots']
                gs_plots = self.env_var.subsitute_env_vars_in_path(gs_plots)
            else:
                gs_plots = os.path.join(trajectory_ouput, 'trajectory_metrics_gs_elevation_plot')

            config['ground_station_plots'] = gs_plots
            logging.info('ground_station_plots: {}'.format(gs_plots))

            if 'radio_source_file' in config.keys():
                radio_source_file = config['radio_source_file']
                radio_source_file = self.env_var.subsitute_env_vars_in_path(radio_source_file)
            else:
                expres_ouput = os.path.join(juice_conf, 'internal', 'expres_tool_wrapper', 'output', crema_id)
                radio_source_file = os.path.join(expres_ouput, 'expres_radio_occ_periods.csv')

            config['radio_source_file'] = radio_source_file
            logging.info('radio_source_file: {}'.format(radio_source_file))

            if 'other_plots' in config.keys():
                other_plots = config['other_plots']
                for i in range(len(other_plots)):
                    other_plots[i] = self.env_var.subsitute_env_vars_in_path(other_plots[i])
            else:
                other_plots = []

            config['other_plots'] = other_plots
            for i in range(len(other_plots)):
                logging.info('other_plots: [{}]: {}'.format(i, other_plots[i]))

        start = end = None

        self.set_mission_phases(start, end, mission_phase_path)
        self.set_traj_info_metric(trajectory_input_path)
        self.get_express_info(radio_source_file, mission_timeline_flyby)
        self.get_coverage_info(coverage_input_path)
        self.gs_plots = gs_plots
        self.set_other_plots(other_plots)

    def set_mission_phases(self, start, end, mission_phase):

        m = MissionPhaseHandler(mission_phase)

        self.mission_phase = m.get_mission_phases()

        self.tour_start, self.tour_end = m.get_tour_period()
        self.gco500_start, self.gco500_end = m.get_ganymede_periods()
        self.tour_sub_phase = m.get_tour_sub_phase()
        self.ganymede_sub_phase = m.get_ganymede_sub_phase()

        if start and end:
            self.reported_period_start = start
            self.reported_period_end = end
        else:
            self.reported_period_start, self.reported_period_end = m.get_all_periods()

        self.my_date_partitions = [self.tour_start, self.gco500_end]

    def set_traj_info_metric(self, trajectory):

        trajectory = TrajectoryInfo(trajectory)

        self.trajectory_info = trajectory.pd2simpledico()
        self.perijove_details = trajectory.pd2perijovedico()
        self.flyby_details = trajectory.pd2fbdico()
        if self.include_cruise:
            self.cruise_details = trajectory.pd2cruisedico()

    def get_coverage_info(self, coverage_input_dir):
        """
        Load Coverage section info

        :param coverage_input_dir:  base dir for coverage files
        """

        if coverage_input_dir == "":

            logging.warning('No coverage_param subsection; input file provided (set "" in configuration file)')

        else:

            list_of_dir = [di for di in os.listdir(coverage_input_dir) if
                           os.path.isdir(os.path.join(coverage_input_dir, di))]

            if not self.include_cruise:
                list_of_dir = [di for di in list_of_dir if 'CRUISE' not in str(di).upper()]

            cov_info = {}

            for di in sorted(list_of_dir):
                current_sub_dir = os.path.join(coverage_input_dir, di)

                cov_info[di] = {}

                list_of_files = [fi for fi in os.listdir(current_sub_dir) if fi.lower().endswith('.png')]

                cov_info[di] = list_of_files

            cov = Coverage(coverage_input_dir, cov_info)

            self.coverage_info = cov

    def get_osve_data_frame(self, eps_package, experiment_type='target'):
        """
        Run OSVE Simulation and get metrics

               We are here going to reuse the osve_wrapper python package to perform a JUICE's EPS simulation

               1) load eps_package info from json file or json data (dico)
                  + run eps if requested (eps is run as part of set_up__from_json_file)

               2) get dataframe

        :param experiment_type: EPS Experiment type (i.e target, instrument)
        :param eps_package: EPS simulation inputs from Juice Timeline Tool
        """

        if eps_package is None:
            message = 'No EPS Metrics subsection; input file provided (set "" in configuration file)'
            logging.warning(message)
            self.report.write_text('\n' + message + '\n')
        else:

            from collections import namedtuple
            o_eps_package = namedtuple('Struct', eps_package.keys())(*eps_package.values())

            here = os.getcwd()
            osve_working_directory = os.path.join(here, o_eps_package.scenario)

            if self.run_simu:  # This flag allows to no run osve simu, but directly get data previously simulated
                run_osve(osve_working_directory, o_eps_package, experiment_type)
            else:
                logging.info('OSVE not Run; OSVE data output get from previous simulation')

            experiment_type_dir = os.path.join(osve_working_directory, experiment_type)
            eps_output_dir = os.path.join(experiment_type_dir, 'eps_output')
            data_avg = os.path.join(eps_output_dir, 'data_rate_avg.out')
            ds_latency = os.path.join(eps_output_dir, 'DS_latency.out')

            dv = DataRateAverage(data_avg)

            self.eps_dataframes = dv

    # def get_eps_data_frame(self, eps_package, experiment_type='target'):
    #     """
    #     Run EPS Simualtion and get metrics
    #
    #            We are here going to reuse the soa_report python package to perform a JUICE's EPS simulation
    #
    #            1) load eps_package info from json file or json data (dico)
    #               + run eps if requested (eps is run as part of set_up__from_json_file)
    #
    #            2) get dataframe
    #
    #     :param experiment_type: EPS Experiment type (i.e target, instrument)
    #     :param eps_package: EPS simulation inputs from Juice Timeline Tool
    #     """
    #
    #     if eps_package['requests']['scenario'] == "":
    #         logging.warning('No EPS Metrics subsection; input file provided (set "" in configuration file)')
    #         self.report.write_text(
    #             '\n' + 'No EPS Metrics subsection; input file provided (set "" in configuration file)' + '\n')
    #     else:
    #
    #         here = os.getcwd()
    #         eps_working_dir = os.path.dirname(eps_package['requests']["root_path"])
    #         os.chdir(eps_working_dir)
    #
    #         eps_package_root = self.load_and_run_eps_simulation(eps_package)
    #
    #         experiment_type_dir = os.path.join(eps_package_root, experiment_type)
    #         eps_output_dir = os.path.join(experiment_type_dir, 'eps_output')
    #         data_avg = os.path.join(eps_output_dir, 'data_rate_avg.out')
    #         ds_latency = os.path.join(eps_output_dir, 'DS_latency.out')
    #
    #         dv = DataRateAverage(data_avg)
    #
    #         self.eps_dataframes = dv
    #
    #         os.chdir(here)

    def get_express_info(self, radio_source_file, mission_timeline_flyby):
        """
        Get Radio source windows opportunities during flybys
        :param mission_timeline_flyby:
        :param radio_source_file:
        """

        if radio_source_file == "":

            logging.warning('No radio Source subsection; input file provided (set "" in configuration file)')

        else:

            self.expres_dataframes = get_radio_source_occ_per_flyby(radio_source_file, mission_timeline_flyby)

    # def load_and_run_eps_simulation(self, eps_package):
    #     """
    #     load eps_package info from json file or json data (dico)
    #        + run eps if requested (eps is run as part of set_up__from_json_file)
    #
    #     :param eps_package: EPS simulation inputs from Juice Timeline Tool
    #     :return: eps_package_root: path of EPS output directory
    #     """
    #
    #     p = EpsPackageHandler()
    #
    #     if isinstance(eps_package, str):
    #
    #         p.set_up__from_json_file(eps_package)
    #
    #     else:
    #
    #         p.set_up_from_parameters(eps_package)
    #
    #     eps_package_root = os.path.join(p.simu.root_path, p.simu.scenario)
    #
    #     return eps_package_root

    def set_other_plots(self, other_plots):

        self.other_plots = other_plots


class Coverage(object):

    def __init__(self, base_dir, info):
        self.base_dir = base_dir
        self.info = info
