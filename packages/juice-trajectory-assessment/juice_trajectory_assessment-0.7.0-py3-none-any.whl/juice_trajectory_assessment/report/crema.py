"""
Created on Jan, 2021

@author: Claudio Munoz Crego (ESAC)

This Module allows to buid a crema object including data for reporting Trajectory Assessment Comparison
"""
import os
import logging

from juice_trajectory_assessment.commons.trajectory_info_handler import TrajectoryInfo
from juice_trajectory_assessment.commons.coverage_info_handler import CoverageInfo
# from old_code.eps_package_handler import EpsPackageHandler
from juice_trajectory_assessment.commons.mission_phases_handler import MissionPhaseHandler
from juice_trajectory_assessment.commons.ca_event_handler import get_radio_source_occ_per_flyby

from soa_report.juice.eps_data.data_rate_avg import DataRateAverage


class Crema(object):

    def __init__(self, crema_id, config, env_var=None, run_simu=True):

        self.crema_id = crema_id

        self.env_var = env_var

        self.mission_phase = None
        self.mission_timeline_flyby = None

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
        self.trajectory_input_path = None

        self.eps_dataframes = None
        self.run_simu = run_simu
        self.expres_dataframes = None

        self.coverage_info = None
        self.coverage_input_path = None

        self.gs_plots = None

        self.wg3_trajectory_metrics_path = ''

        self.data_volume_overview_path = None
        self.trajectory_overview_path = None
        self.perijove_plots_path = None
        self.wg3_trajectory_plots_path = None
        self.wg4_trajectory_plots_path = None

        self.radio_source_file = None

        self.other_plots = None

        self.stellar_occs_plots = None

        self.perijove_details = None
        self.flyby_details = None
        self.cruise_details = None

        self.simu = None
        self.simu_package = None

        self.include_cruise = False

        self.docx_template = None

        self.generate_pdf = False

        self.set_crema(config)

    def set_crema(self, config):

        config_main = config['main']

        if 'eps_package_param' in config.keys():
            eps_package_param = config['eps_package_param']

            self.simu = 'eps'
            self.simu_package = eps_package_param

            mission_phase_path = config_main['mission_phase']
            self.mission_timeline_flyby = config_main['mission_timeline_flyby']
            self.trajectory_input_path = config_main['trajectory_input_file']
            self.coverage_input_path = config_main['coverage_input_dir']
            self.gs_plots = config_main['ground_station_plots']
            other_plots = config_main['other_plots']
            self.radio_source_file = config_main['radio_source_file']

            if 'wg3_trajectory_metrics' in config_main.keys():
                self.wg3_trajectory_metrics_path = config_main['wg3_trajectory_metrics']

        if 'osve' in config.keys():

            osve_params = config['osve']

            if self.env_var and 'path_eps_brf' in osve_params.keys():

                path_eps_brf = osve_params['path_eps_brf']
                tmp = self.env_var.subsitute_env_vars_in_path(path_eps_brf)
                tmp = os.path.abspath(tmp)
                osve_params['path_eps_brf'] = tmp

            self.simu = 'osve'
            self.simu_package = osve_params

            crema_id = osve_params["crema_id"]
            crema_id_x_y = crema_id.replace('crema_', '')

            osve_params["juice_conf"] = self.env_var.subsitute_env_vars_in_path(osve_params["juice_conf"])

            if 'local_root_dir' in osve_params['kernel']:
                osve_params['kernel']['local_root_dir'] = \
                    self.env_var.subsitute_env_vars_in_path(osve_params['kernel']['local_root_dir'])

            juice_conf = osve_params["juice_conf"]
            geopipeline_output = os.path.join(juice_conf, 'internal', 'geopipeline', 'output', crema_id)
            trajectory_ouput = os.path.join(geopipeline_output, 'trajectory')
            trajectory_input = os.path.join(juice_conf, 'internal', 'trajectory_reporter', 'input', crema_id)
            coverage_ouput = os.path.join(juice_conf, 'internal', 'coverage_tool', 'output', crema_id, 'trajectory_assessment')
            timeline_ouput = os.path.join(juice_conf, 'internal', 'timeline', 'output', crema_id)

            if 'ptr' in osve_params.keys():
                osve_params['ptr'] = self.env_var.subsitute_env_vars_in_path(osve_params['ptr'])
            else:
                osve_params['ptr'] = os.path.join(timeline_ouput,
                                                  'spice_segmentation_attitude_{}.ptx'.format(str(crema_id_x_y)))

            if 'no_ptr_cut' not in osve_params.keys():
                osve_params['no_ptr_cut'] = False  # by default enforce cut PTR to the TOP_ITL start/end times

            mission_phase_path = \
                os.path.join(juice_conf, 'internal', 'geopipeline', 'output', crema_id, 'Mission_Phases.csv')
            mission_phase_path = self.reset_input_file_path(config_main, 'mission_phase', mission_phase_path)

            mission_timeline_event_file_name = 'mission_timeline_event_file_{}.csv'.format(crema_id_x_y)
            self.mission_timeline_flyby = os.path.join(geopipeline_output, mission_timeline_event_file_name)
            self.mission_timeline_flyby = \
                self.reset_input_file_path(config_main, 'mission_timeline_flyby', self.mission_timeline_flyby)

            self.wg3_trajectory_metrics_path = os.path.join(trajectory_ouput, 'wg3_trajectory_metrics')
            self.wg3_trajectory_metrics_path = \
                self.reset_input_file_path(config_main, 'wg3_trajectory_metrics', self.wg3_trajectory_metrics_path)

            trajectory_input_file_name = 'trajectory_metrics_data_{}.csv'.format(crema_id_x_y)
            self.trajectory_input_path = os.path.join(trajectory_ouput, trajectory_input_file_name)
            self.trajectory_input_path = \
                self.reset_input_file_path(config_main, 'trajectory_input_file', self.trajectory_input_path)

            self.set_traj_info_metric(self.trajectory_input_path)

            self.coverage_input_path = coverage_ouput
            self.coverage_input_path = \
                self.reset_input_file_path(config_main, 'coverage_input_dir', self.coverage_input_path)

            self.gs_plots = os.path.join(trajectory_ouput, 'trajectory_metrics_gs_elevation_plot')
            self.gs_plots = self.reset_input_file_path(config_main, 'ground_station_plots', self.gs_plots)

            self.data_volume_overview_path = os.path.join(trajectory_input, 'data_volume_overview')
            self.data_volume_overview_path = \
                self.reset_input_file_path(config_main, 'data_volume_overview', self.data_volume_overview_path)

            self.trajectory_overview_path = os.path.join(trajectory_input, 'trajectory_overview')
            self.trajectory_overview_path = \
                self.reset_input_file_path(config_main, 'trajectory_overview', self.trajectory_overview_path)

            self.perijove_plots_path = os.path.join(trajectory_input, 'trajectory', 'perijove_plots')
            self.perijove_plots_path = \
                self.reset_input_file_path(config_main, 'perijove_plots', self.perijove_plots_path)

            self.wg3_trajectory_plots_path = os.path.join(trajectory_input, 'trajectory', 'wg3_trajectory_plots')
            self.wg3_trajectory_plots_path = \
                self.reset_input_file_path(config_main, 'wg3_trajectory_plots', self.wg3_trajectory_plots_path)

            self.wg4_trajectory_plots_path = os.path.join(trajectory_input, 'trajectory', 'wg4_trajectory_plots')
            self.wg4_trajectory_plots_path = \
                self.reset_input_file_path(config_main, 'wg4_trajectory_plots', self.wg4_trajectory_plots_path)

            self.stellar_occs_plots = os.path.join(trajectory_ouput, 'stellar_occs_plots')
            self.stellar_occs_plots = \
                self.reset_input_file_path(config_main, 'stellar_occs_plots', self.stellar_occs_plots)

            expres_output = os.path.join(juice_conf, 'internal', 'expres_tool_wrapper', 'output', crema_id)
            self.radio_source_file = os.path.join(expres_output, 'expres_radio_occ_periods.csv')
            self.radio_source_file = \
                self.reset_input_file_path(config_main, 'radio_source_file', self.radio_source_file)

            is_wg4_trajectory_metrics_plots_specified = False
            if 'other_plots' in config_main.keys():

                other_plots = config_main['other_plots']

                for i in range(len(other_plots)):

                    other_plots[i] = self.env_var.subsitute_env_vars_in_path(other_plots[i])

                    if 'wg4_trajectory_metrics_plots' in other_plots[i]:
                        is_wg4_trajectory_metrics_plots_specified = True
            else:
                other_plots = []

            if not is_wg4_trajectory_metrics_plots_specified:
                other_plots.insert(0, os.path.join(trajectory_ouput, 'wg4_trajectory_metrics_plots'))

            for i in range(len(other_plots)):
                logging.info('other_plots: [{}]: {}'.format(i, other_plots[i]))

            if 'docx_template' in config_main.keys():
                self.docx_template = config_main['docx_template']

            if 'generate_pdf' in config_main.keys():
                self.generate_pdf = config_main['generate_pdf']

            if 'include_cruise' in config_main.keys():
                self.include_cruise = config_main['include_cruise']

        start = end = None

        self.set_mission_phases(start, end, mission_phase_path)
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

            cov_info = {}

            for di in sorted(list_of_dir):

                current_sub_dir = os.path.join(coverage_input_dir, di)

                cov_info[di] = {}

                list_of_files = [fi for fi in os.listdir(current_sub_dir) if fi.lower().endswith('.json')]

                for f in sorted(list_of_files):
                    coverage_param = os.path.join(current_sub_dir, f)
                    cov_info_metric = CoverageInfo(coverage_param).dico2metric()
                    cov_info_metric = [v for v in cov_info_metric if
                                       v[0] not in ['metakernel', 'map', 'output_path_figure']]

                    cov_info[di][f] = cov_info_metric

            cov = Coverage(coverage_input_dir, cov_info)

            self.coverage_info = cov

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

        # rime_ajs = get_rime_opp(radio_source_file, mission_timeline_flyby)
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
    #         p.set_up_from_json_file(eps_package)
    #
    #     else:
    #
    #         p.set_up_from_parameters(eps_package)
    #
    #     eps_package_root = os.path.join(p.simu.root_path, p.simu.scenario)
    #
    #     return eps_package_root

    def reset_input_file_path(self, config_main, data_name, input_path):
        """
        Reset input data path if defined in local configuration

        :param config_main: configuration file structure
        :param data_name: data file name
        :param input_path: data file path (default from gitlab conf repository)
        :return: input_path: data file path
        """

        if data_name in config_main.keys():
            input_path = config_main[data_name]
            input_path = self.env_var.subsitute_env_vars_in_path(input_path)

        logging.info(f'{data_name}: {input_path}')

        return input_path

    def set_other_plots(self, other_plots):

        self.other_plots = other_plots


class Coverage(object):

    def __init__(self, base_dir, info):
        self.base_dir = base_dir
        self.info = info
