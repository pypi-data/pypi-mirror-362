"""
Created on July 2020

@author: Claudio Munoz Crego (ESAC)

This Module allows to report trajectory assessment subsection including plots
"""

import logging
import os
import shutil
import sys

from tabulate import tabulate

from old_code.eps_package_handler import EpsPackageHandler
from juice_trajectory_assessment.report.basic_report import BasicReport
from juice_trajectory_assessment.report.crema import Crema
from juice_trajectory_assessment.report.rst_report import RstReport
from osve_wrapper.osve_advanced_wrapper import run_osve
from soa_report.juice.eps_data.data_rate_avg import DataRateAverage


class TrajAssessmentFilter(BasicReport):
    """
    This class allows to report trajectory assessment using SOC simulation Metrics
    """

    def __init__(self, start, end, env_var, output_dir='./'):

        self.env_var = env_var

        self.plots_path = None

        self.crema_ref = None

        BasicReport.__init__(self, start, end, output_dir=output_dir)

    def set_crema_ref(self, id, config, run_simu=True):
        """
        Set Crema object

        :param id: Crema Identifier
        :param config: crema specific parameters
        :param run_simu: Flag to enforce/avoid osve simulation; Default is True
        """

        self.crema_ref = Crema(id, config, env_var=self.env_var, run_simu=run_simu)

    def create_report(self, working_dir,
                      output_dir='',
                      report_title='Trajectory Assessment',
                      objective='',
                      new_report_name=None):
        """
        Creates Trajectory Assessment reports

        :param working_dir: working directory
        :param report_title: title report
        :param new_report_name: report file name
        :param output_dir: path of output directory (there is a default values)
        :param objective: optional text to be added at the beginning of the report
        """

        (trajectory, output_dir, self.plots_path) = self.set_up_parameters(self.crema_ref.trajectory_input_path,
                                                                           output_dir)

        self.report = RstReport(self.plots_path, out='rst', output_path=output_dir)

        self.report.print_summary_intro(report_title, objective)

        self.report.write_head(2, 'Trajectory Summary')
        self.fill_generic_subsection(self.crema_ref.trajectory_overview_path)

        self.report.write_head(3, 'Main Parameters')
        self.report.write_text('\nThis section provides a list of trajectory parameters.\n')
        traj_info_metric = self.crema_ref.trajectory_info

        self.report.print_rst_table_2(traj_info_metric)

        self.add_perijove_details()

        self.fill_generic_subsection(self.crema_ref.perijove_plots_path)

        self.add_flyby_details()

        if self.crema_ref.include_cruise:
            self.add_cruise_flyby_details()

        self.add_express_subsection(self.crema_ref.radio_source_file, self.crema_ref.mission_timeline_flyby)


        self.report.write_head(2, 'Downlink capacity')

        if self.crema_ref.simu == 'eps':

            self.fill_eps_metric_section(self.crema_ref.simu_package)

        elif self.crema_ref.simu == 'osve':

            self.fill_osve_metric_section(working_dir, self.crema_ref.simu_package, experiment_type='target')

        else:

            self.report.write_text('\n No EPS output \n\n')

        self.fill_generic_subsection(self.crema_ref.data_volume_overview_path)


        self.report.write_head(2, 'Moons surface coverage')
        self.report.write_text('\n The following figures provide a trace of the ground track as JUICE swings by the different'
                                'moons.  The track is colored as a function of altitude from the moon’s surface, see the legend.\n\n')


        self.fill_coverage_section(self.crema_ref.coverage_input_path)

        self.report.write_head(2, 'ANNEX')
        self.fill_annex_ground_station_plots(self.crema_ref.gs_plots)
        self.fill_wg3_trajectory_metrics(self.crema_ref.wg3_trajectory_metrics_path)
        for i_plot in self.crema_ref.other_plots:
            self.fill_generic_subsection(i_plot)

        self.fill_generic_subsection(self.crema_ref.wg3_trajectory_plots_path)
        self.fill_generic_subsection(self.crema_ref.wg4_trajectory_plots_path)

        self.fill_stellar_occultation(self.crema_ref.stellar_occs_plots)

        self.report.print_summary_end()
        self.report.rst_to_html()

        # PDF report removed from version 0.5.6
        # if self.crema_ref.generate_pdf:
        #     self.report.rst2pdf(self.get_template_rst2pdf())

        if self.crema_ref.docx_template:
            docx_style_file = self.crema_ref.docx_template
        else:
            docx_style_file = self.get_template_docx()

        self.report.pandoc_html_to_docx(docx_style_file=docx_style_file)

        if new_report_name:
            self.report.rename_report(new_report_name, just_rename=True)

    def add_express_subsection(self, radio_source_file, mission_timeline_flyby):
        """
        Add a subsection with Radio source windows opportunities during flybys
        :param radio_source_file: radio source input file path
        :param mission_timeline_flyby: mission timeline input file path
        """
        from juice_trajectory_assessment.commons.ca_event_handler import get_radio_source_occ_per_flyby

        # rime_ajs = get_rime_opp(radio_source_file, mission_timeline_flyby)
        if radio_source_file == "":

            logging.warning('No radio Source subsection; input file provided (set "" in configuration file)')

        else:
            df = get_radio_source_occ_per_flyby(radio_source_file, mission_timeline_flyby)

            self.report.write_head(3, 'Radio Source Parameters')

            self.report.write_text('\n This section provides time periods, as simulated by the ExPress tool, '
                                   'where JUICE is within +/- 12 hours around a moon CA flybys and '
                                   'when the targeted moon is occulting all Jupiter radio sources within frequency'
                                   ' range [9-11 MHz]. Flybys during which at least one of the Jupiter radio sources'
                                   ' is always visible from JUICE do not appear below.\n\n')

            my_tab = tabulate(df, headers='keys', tablefmt='grid', numalign='center',
                              stralign='center',
                              showindex=False)

            self.report.write_text('\n' + my_tab + '\n')

    def fill_coverage_section(self, coverage_input_dir):
        """
        Fill Coverage section

        :param coverage_input_dir:
        """

        list_of_dir = []

        if coverage_input_dir == "":
            logging.warning('No coverage_param subsection; input file provided (set "" in configuration file)')
            self.report.write_text(
                '\n' + 'No coverage_param metrics; input file provided (set "" in configuration file)' + '\n')
        else:

            list_of_dir = [di for di in os.listdir(coverage_input_dir) if
                           os.path.isdir(os.path.join(coverage_input_dir, di))]

            if not self.crema_ref.include_cruise:
                list_of_dir = [di for di in list_of_dir if 'CRUISE' not in str(di).upper()]

        for di in sorted(list_of_dir):

            self.report.write_head(3, di.split('-')[1].capitalize())
            current_sub_dir = os.path.join(coverage_input_dir, di)

            list_of_files = [fi for fi in os.listdir(current_sub_dir) if fi.lower().endswith('.png')]

            for f in sorted(list_of_files):

                coverage_param = os.path.join(current_sub_dir, f)

                if 'CRUISE' in di:
                    tmp_name = f.split('.')[0].split('__')
                    id_trajectory = tmp_name[0]
                    id_phase = 'Cruise'
                    id_parameter = 'Flyby ' + tmp_name[2]
                    id_target = tmp_name[3].capitalize()
                else:
                    tmp_name = f.split('.')[0].split('__')
                    id_trajectory = tmp_name[0]
                    id_phase = tmp_name[1]
                    id_parameter = tmp_name[2]
                    if id_phase == "tour":
                        id_target = str(tmp_name[3]).capitalize()
                    else:
                        id_target = str(di.split('-')[1]).capitalize()

                title = '{} {}'.format(id_target.capitalize(), id_parameter.capitalize())

                description = "Coverage of {} surface ({}) for crema_{}: {}.".format(
                    id_target, id_phase, id_trajectory, id_parameter)

                self.report.write_head(4, title)

                coverage_plot = coverage_param

                if coverage_plot:
                    source = coverage_plot
                    dst = os.path.join(self.plots_path, os.path.basename(source))
                    shutil.copy(source, dst)

                    self.report.rst_insert_figure(dst, description, text="")

    def fill_eps_metric_section(self, eps_package, experiment_type='target'):
        """
        Report EPS metrics

        We are here going to reuse the soa_report python package to perform a JUICE's EPS simulation

        1) load eps_package info from json file or json data (dico)
           + run eps if requested (eps is run as part of set_up__from_json_file)

        2) get dataframe

        :param experiment_type: EPS Experiment type (i.e target, instrument)
        :param eps_package: EPS simulation inputs from Juice Timeline Tool
        """

        if eps_package['requests']['scenario'] == "":
            logging.warning('No EPS Metrics subsection; input file provided (set "" in configuration file)')
            self.report.write_text(
                '\n' + 'No EPS Metrics subsection; input file provided (set "" in configuration file)' + '\n')
        else:

            eps_package_root = self.load_and_run_eps_simulation(eps_package)

            experiment_type_dir = os.path.join(eps_package_root, experiment_type)
            eps_output_dir = os.path.join(experiment_type_dir, 'eps_output')
            data_avg = os.path.join(eps_output_dir, 'data_rate_avg.out')
            ds_latency = os.path.join(eps_output_dir, 'DS_latency.out')

            dv = DataRateAverage(data_avg)

            my_date_partitions = [self.crema_ref.reported_period_start, self.crema_ref.reported_period_end]
            data_frames = self.get_periods(dv, my_date_partition=my_date_partitions)

            self.report_summary_table(data_frames, title='Downlink Capacity in Gbits for the Reported period')

            # tour
            my_date_partitions = [self.crema_ref.tour_start, self.crema_ref.tour_end]
            data_frames = self.get_periods(dv, my_date_partition=my_date_partitions)

            text = ''

            self.report_summary_table(data_frames, title='Downlink Capacity in Gbits for the Tour', text=text)
            # self.report_summary_table(data_frames,
            # title='Generated DV, downlink, and SSM status in Gbits for the Tour')

            self.report_sub_phases_table_dowlink_capacity(dv, self.crema_ref.tour_sub_phase,
                                                          title='Downlink Capacity [Gbits] per sub-phases of Tour')

            # Ganymede
            my_date_partitions = [self.crema_ref.gco500_start, self.crema_ref.gco500_end]
            data_frames = self.get_periods(dv, my_date_partition=my_date_partitions)

            self.report_summary_table(data_frames, title='Downlink Capacity in Gbits for the Ganymede phase')

            self.report_sub_phases_table_dowlink_capacity(
                dv,
                self.crema_ref.ganymede_sub_phase,
                title='Downlink Capacity [Gbits] per sub-phases of Ganymede Phase')

    def fill_osve_metric_section(self, working_dir, eps_package, experiment_type='target'):
        """
        Report EPS metrics

        We are here going to reuse the soa_report python package to perform a JUICE's EPS simulation

        1) load eps_package info from json file or json data (dico)
           + run eps if requested (eps is run as part of set_up__from_json_file)

        2) get dataframe

        :param working_dir: working directory
        :param experiment_type: EPS Experiment type (i.e target, instrument)
        :param eps_package: EPS simulation inputs from Juice Timeline Tool
        """

        if eps_package is None:
            logging.warning('No EPS Metrics subsection; input file provided (set "" in configuration file)')
            self.report.write_text(
                '\n' + 'No EPS Metrics subsection; input file provided (set "" in configuration file)' + '\n')
        else:

            from collections import namedtuple
            o_eps_package = namedtuple('Struct', eps_package.keys())(*eps_package.values())

            osve_working_directory = os.path.join(working_dir, o_eps_package.scenario)
            if self.crema_ref.run_simu:
                run_osve(osve_working_directory, o_eps_package, experiment_type)
            else:
                logging.info('OSVE not Run; OSVE data output get from previous simulation')

            experiment_type_dir = os.path.join(osve_working_directory, experiment_type)
            eps_output_dir = os.path.join(experiment_type_dir, 'eps_output')
            data_avg = os.path.join(eps_output_dir, 'data_rate_avg.out')
            ds_latency = os.path.join(eps_output_dir, 'DS_latency.out')

            dv = DataRateAverage(data_avg)

            my_date_partitions = [self.crema_ref.reported_period_start, self.crema_ref.reported_period_end]
            data_frames = self.get_periods(dv, my_date_partition=my_date_partitions)

            self.report_summary_table(data_frames, title='Downlink Capacity in Gbits for the Reported period')

            # tour
            my_date_partitions = [self.crema_ref.tour_start, self.crema_ref.tour_end]
            data_frames = self.get_periods(dv, my_date_partition=my_date_partitions)

            text = ''

            self.report_summary_table(data_frames, title='Downlink Capacity in Gbits for the Tour', text=text)
            # self.report_summary_table(data_frames,
            # title='Generated DV, downlink, and SSM status in Gbits for the Tour')

            self.report_sub_phases_table_dowlink_capacity(dv, self.crema_ref.tour_sub_phase,
                                                          title='Downlink Capacity [Gbits] per sub-phases of Tour')

            # Ganymede
            my_date_partitions = [self.crema_ref.gco500_start, self.crema_ref.gco500_end]
            data_frames = self.get_periods(dv, my_date_partition=my_date_partitions)

            self.report_summary_table(data_frames, title='Downlink Capacity in Gbits for the Ganymede phase')

            self.report_sub_phases_table_dowlink_capacity(
                dv, self.crema_ref.ganymede_sub_phase,
                title='Downlink Capacity [Gbits] per sub-phases of Ganymede Phase')

    def fill_annex_ground_station_plots(self, gs_plots):
        """
        Report Ground Stations elevation and Visibility Limit plots

        :param gs_plots: Ground Stations elevation and Visibility Limit plots
        """

        if os.path.exists(gs_plots):

            self.report.write_head(3, 'Ground Stations elevation and Visibility Limit ')

            self.report.write_text('\n\nThis subsection contains Ground Stations elevation and'
                                   ' visibility limit for each flyby of the Tour\n\n')

            list_of_plots = os.listdir(gs_plots)
            to_sort = []

            for f in list_of_plots:
                if not str(f).startswith('.ipynb'):
                    flyby_index = f.replace('.png', '').replace('Flyby_stations_elevation_', '')
                    f_index = float(''.join([c for c in flyby_index if c.isnumeric()]))
                    to_sort.append([f_index, flyby_index, f])

            sorted_list = sorted(to_sort)

            for [f_index, flyby_index, f] in sorted_list:
                fi = os.path.join(gs_plots, f)
                fi_title = 'Ground Stations elevation and Visibility Limit: {}\n'.format(flyby_index)
                fig = os.path.expandvars(fi)
                # self.report.print_summary_sub_subsection(fi_title, figure=[fig])
                dst = os.path.join(self.plots_path, f)
                shutil.copy(fig, dst)
                self.report.rst_insert_figure(dst, text='', title=fi_title)

            logging.info('Plot directory processed {}'.format(gs_plots))

        else:

            logging.warning('Plot directory does not exits: {}'.format(gs_plots))

    def fill_generic_subsection(self, plot_dir):
        """
        Report more plots within ANNEX section from directory

        :param plot_dir: directory where plot are located
        """

        if os.path.exists(plot_dir):

            base_name = (os.path.basename(plot_dir)).replace('_', ' ').capitalize()

            base_name = base_name.replace('Wg', 'WG')

            self.report.write_head(3, base_name)

            list_of_plots = os.listdir(plot_dir)

            # check if txt and/or csv file in list_of_plots:
            list_of_txt_files = [f for f in list_of_plots if f.endswith(".txt")]
            list_of_csv_files = [f for f in list_of_plots if f.endswith(".csv")]
            list_of_plots = [f for f in list_of_plots if f.endswith(".png")]
            list_of_plots.sort()

            for f_txt in list_of_txt_files:

                fi = open(os.path.join(plot_dir, f_txt), 'r')
                self.report.write_text('\n')

                for line in fi.readlines():
                    if line.startswith('....'):
                        line = '\n'
                    self.report.write_text(line)

                self.report.write_text('\n')
                fi.close()

            import pandas as pd
            for f_csv in sorted(list_of_csv_files):
                fi = open(os.path.join(plot_dir, f_csv), 'r')
                df = pd.read_csv(fi, sep=";", comment='#', skip_blank_lines=True)
                for k in list(df.keys()):
                    df = df[k].str.replace('^..+', '', regex=True)  # remove row where = ....
                # df.replace('^\.\.+', '', regex=True)
                # df = df.apply(pd.to_numeric, errors='coerce')
                # df = df.dropna()
                my_tab = tabulate(df, headers='keys', tablefmt='grid', numalign='center',
                                  stralign='center',
                                  showindex=False)

                self.report.write_text('\n' + my_tab + '\n')
                fi.close()

            for f in list_of_plots:
                if not str(f).startswith('.ipynb'):
                    fi_title = (os.path.basename(f)).replace('.png', '')
                    fi = os.path.join(plot_dir, f)
                    fi_title = '{}\n'.format(fi_title)
                    fig = os.path.expandvars(fi)
                    dst = os.path.join(self.plots_path, f)
                    shutil.copy(fig, dst)
                    self.report.rst_insert_figure(dst, text='', title='')

            logging.info('Plot directory processed {}'.format(plot_dir))

        else:

            logging.warning('Plot directory does not exits: {}'.format(plot_dir))

    def fill_wg3_trajectory_metrics(self, wg3_trajectory_metrics_path):
        """
        Fill Coverage section

        :param wg3_trajectory_metrics_path: wg3 file path
        """

        self.report.write_head(3, 'WG3 trajectory metrics summary')

        if wg3_trajectory_metrics_path == "":
            logging.warning('No wg3_trajectory_metrics subsection; input file provided (set "" in configuration file)')
            self.report.write_text(
                '\n' + 'No wg3_trajectory_metrics metrics; input file provided (set it in configuration file)' + '\n')
        else:

            # We maintain here csv and txt extension for backward compatibility
            # csv are included as is in the report
            input_file_csv = os.path.join(wg3_trajectory_metrics_path, 'wg3_trajectory_metrics_text.csv')
            input_file_txt = os.path.join(wg3_trajectory_metrics_path, 'wg3_trajectory_metrics_text.txt')

            fi = None

            if os.path.exists(input_file_csv):

                fi = open(input_file_csv)

            elif os.path.exists(input_file_txt):

                fi = open(input_file_txt)

                for line in fi.readlines():
                    if line.startswith('....'):
                        line = '\n'
                    self.report.write_text(line)

                fi.close()

            else:
                logging.error(f'WG3 trajectory metrics file does not exist; not reported: '
                              f'{input_file_txt}')

            list_of_png_files = [fi for fi in os.listdir(wg3_trajectory_metrics_path) if fi.lower().endswith('.png')]

            for f in sorted(list_of_png_files):
                file_path = os.path.join(wg3_trajectory_metrics_path, f)
                title = ''.join(f.split('-')).capitalize()

                dst = os.path.join(self.plots_path, f)
                shutil.copy(file_path, dst)

                self.report.rst_insert_figure(dst, title, text="")

    def fill_stellar_occultation(self, stellar_occs_path):
        """
        Fill Stellar Occultation plots section

        :param stellar_occs_path:
        """

        self.report.write_head(3, 'Stellar Occultation Plots')

        if stellar_occs_path == "":
            logging.warning('No stellar_occs_plots subsection; input file provided (set "" in configuration file)')
            self.report.write_text(
                '\n' + 'No stellar_occs_plots metrics; input file provided (set it in configuration file)' + '\n')
        else:

            list_of_png_files = [fi for fi in os.listdir(stellar_occs_path) if fi.lower().endswith('.png')]

            for f in sorted(list_of_png_files):
                file_path = os.path.join(stellar_occs_path, f)
                title = ''.join(f.split('-')).capitalize()

                dst = os.path.join(self.plots_path, f)
                shutil.copy(file_path, dst)

                self.report.rst_insert_figure(dst, title, text="")

    def add_perijove_details(self):
        """
        Add details on Flybys and Perijoves
        """

        # headers = ['Event', 'value']
        self.report.insert_page_break()

        self.report.write_head(3, 'Perijove geometry summary')
        self.report.write_text("\n")

        self.report.print_rst_table_2(self.crema_ref.perijove_details)

    def add_flyby_details(self):
        """
        Add details on Flybys and Perijoves
        """

        self.report.insert_page_break()

        self.report.write_head(3, 'Flybys geometry summary')
        self.report.write_text("\n")

        self.report.print_rst_table_2(self.crema_ref.flyby_details)

    def add_cruise_flyby_details(self):
        """
        Add details on Cruise Flybys
        """
        self.report.insert_page_break()

        self.report.write_head(3, 'Cruise Flybys Summary')
        self.report.write_text("Method used to identify cruise flybys:\n"
                               "Currently the geopipeline identifies the cruise flybys by searching for local minimum"
                               " (altitude < 20000 km).\n")
        self.report.write_text("\n")

        self.report.print_rst_table_2(self.crema_ref.cruise_details)

    def load_and_run_eps_simulation(self, eps_package):
        """
        load eps_package info from json file or json data (dico)
           + run eps if requested (eps is run as part of set_up__from_json_file)

        :param eps_package: EPS simulation inputs from Juice Timeline Tool
        :return: eps_package_root: path of EPS output directory
        """

        p = EpsPackageHandler(self.output_dir)

        if isinstance(eps_package, str):

            p.set_up_from_json_file(eps_package)

        else:

            p.set_up_from_parameters(eps_package)

        eps_package_root = os.path.join(p.simu.root_path, p.simu.scenario)

        return eps_package_root

    def get_template_rst2pdf(self):
        """
        Get the rst2pdf.style template hosted in source code within templates sub-directory

        :return: rst2pdf.style  path
        :rtype: python path
        """

        here = os.path.abspath(os.path.dirname(__file__))
        template_file = os.path.join(here, 'templates')
        template_file = os.path.join(template_file, 'default_rst2pdf.style')

        if not os.path.exists(template_file):
            logging.error('reference template file "%s" missing' % template_file)
            sys.exit()

        logging.info('{} loaded'.format(template_file))

    def get_template_docx(self):
        """
        Get the style.docx template hosted in source code within templates sub-directory

        :param: orientation_landscape: Flag to enforce A4 landscape orientation; default False
        :return: style.docx   path
        :rtype: python path
        """

        default_template = 'custom-reference.docx'

        here = os.path.abspath(os.path.dirname(__file__))
        template_file = os.path.join(here, 'templates')
        template_file = os.path.join(template_file, default_template)

        if not os.path.exists(template_file):
            logging.error('reference template file "%s" missing' % template_file)
            sys.exit()

        logging.info('{} loaded'.format(template_file))

        return template_file

    def set_up_parameters(self, trajectory, output_dir='./'):
        """
        Set up parameters

        :param trajectory: path of the trajectory input file generated by geopipeline
        :param output_dir: path of output directory (there is a default values)
        :return: scenario, root_path, output_dir, plots_path
        """

        if not os.path.exists(trajectory):
            logging.error('bad trajectory file: {}'.format(trajectory))

        output_dir = os.path.expandvars(output_dir)
        if not os.path.exists(output_dir):
            logging.warning('output dir does not exist: {}'.format(output_dir))
            output_base_dir = os.path.dirname(output_dir)

            if os.path.exists(output_base_dir):
                logging.warning('output base directory exist; Trying to create output dir: {}'.format(output_dir))
                os.mkdir(output_dir)

            else:

                logging.error("Output dir nor output base directory exist; "
                              "Please check output_dir in config file".format(output_dir))
                sys.exit()

        plots_path = os.path.join(output_dir, 'plots')
        if not os.path.exists(plots_path):
            os.mkdir(plots_path)

        return trajectory, output_dir, plots_path
