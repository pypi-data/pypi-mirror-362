"""
Created on Jan, 202

@author: Claudio Munoz Crego (ESAC)

This Module allows to report Trajectory Assessment Comparison subsection including plots
"""

import logging
import os
import shutil
import sys
from operator import itemgetter

import pandas as pd
from tabulate import tabulate

from juice_trajectory_assessment.comparison_report.basic_comparison_report import BasicComparisonReport
from juice_trajectory_assessment.comparison_report.crema import Crema
from juice_trajectory_assessment.report.rst_report import RstReport


class ComparisonReport(BasicComparisonReport):
    """
    This class allows to report trajectory assessment using SOC simulation Metrics
    """

    def __init__(self, start, end, env_var, output_dir='./',
                 juice_conf=None, path_to_osve_lib_dir=None, kernel_root_dir=None):

        self.env_var = env_var

        self.plots_path = None

        self.crema_ref = None
        self.crema_2compare = None

        BasicComparisonReport.__init__(self, start, end, output_dir=output_dir)

    def set_crema_ref(self, id, config, juice_conf=None, path_to_osve_lib_dir=None,
                      kernel=None, run_simu=True, include_dv_section=True, include_cruise=False):
        """
        Set Crema object

        :param id: Crema Identifier
        :param config: crema specific parameters
        :param juice_conf: path of juice configuration
        :param path_to_osve_lib_dir: path of osve lib
        :param kernel: kernel parameters
        :param run_simu: Flag to enforce/avoid osve simulation; Default is True
        :param include_dv_section: Flag to enforce/avoid DV section; Default is True; If set to False run_simu
        :param include_cruise: Flag to enforce/avoid Cruise section; Default is False
        ignored and set to False
        """

        self.crema_ref = Crema(id, config, env_var=self.env_var,
                               juice_conf=juice_conf, path_to_osve_lib_dir=path_to_osve_lib_dir,
                               kernel=kernel, run_simu=run_simu,
                               include_dv_section=include_dv_section, include_cruise=include_cruise)

    def set_crema_2compare(self, id, config, juice_conf=None, path_to_osve_lib_dir=None,
                           kernel=None, run_simu=True, include_dv_section=True, include_cruise=False):
        """
        Set Crema object

        :param id: Crema Identifier
        :param config: crema specific parameters
        :param juice_conf: path of juice configuration
        :param path_to_osve_lib_dir: path of osve lib
        :param kernel: kernel parameters
        :param run_simu: Flag to enforce/avoid osve simualtion; Default is True
        :param include_dv_section: Flag to enforce/avoid DV section; Default is True; If se to False run_simu
        ignored and set to False
        :param include_cruise: Flag to enforce/avoid Cruise section; Default is False
        """

        self.crema_2compare = Crema(id, config, env_var=self.env_var,
                                    juice_conf=juice_conf, path_to_osve_lib_dir=path_to_osve_lib_dir,
                                    kernel=kernel, run_simu=run_simu,
                                    include_dv_section=include_dv_section, include_cruise=include_cruise)

    def create_report(self,
                      root_path,
                      output_dir='',
                      report_title='Trajectory Assessment',
                      report_orientation_landscape=False,
                      new_report_name=None,
                      docx_template=None,
                      generate_pdf=False):
        """
        Creates Trajectory Assessment Comparison reports


        :param new_report_name: Report file name without extension
        :param root_path: base directory of scenario
        :param output_dir: path of output directory (there is a default values)
        :param report_title: Report title
        :param report_orientation_landscape: Flag to enforce A4 landscape orientation; default False
        :param docx_template: path to docx template file
        :param generate_pdf: flag to generate pdf report; False by default
        """

        (root_path, output_dir, self.plots_path) = self.set_up_parameters(root_path, output_dir)

        self.report = RstReport(self.plots_path, out='rst', output_path=output_dir)

        objective = ''  # ''Report Trajectory Assessment Report for Juice Mission'
        self.report.print_summary_intro(report_title, objective)

        self.report.write_head(2, 'Trajectory Summary')
        self.report.write_text('\nThis section provides a list of trajectory parameters.\n')
        self.report.write_head(3, 'Main Parameters')
        traj_info_metric = self.crema_ref.trajectory_info
        traj_info_metric_2 = self.crema_2compare.trajectory_info

        traj_info_metric[0][1] = 'values {}'.format(self.crema_ref.crema_id)
        traj_info_metric[0].append('values {}'.format(self.crema_2compare.crema_id))
        for i in range(1, len(traj_info_metric)):
            traj_info_metric[i].append(traj_info_metric_2[i][1])

        self.report.print_rst_table_2(traj_info_metric)

        self.add_perijove_flyby_details(self.crema_ref)
        self.add_perijove_flyby_details(self.crema_2compare)

        if self.crema_ref.include_cruise:
            self.add_cruise_flyby_details(self.crema_ref)
            self.add_cruise_flyby_details(self.crema_2compare)

        self.add_express_subsection()

        if self.crema_ref.include_dv_section:
            self.report.write_head(2, 'Downlink capacity')
            self.fill_eps_metric_section()
        else:
            logging.info('DV section no included')

        self.report.write_head(2, 'Moons surface coverage')
        self.fill_coverage_section()

        self.report.write_head(2, 'ANNEX')
        # self.fill_annex_ground_station_plots(self.crema_ref.gs_plots)
        for i_plot in self.crema_ref.other_plots:
            self.fill_annex_plots(i_plot, self.crema_ref.tour_sub_phase)

        for i_plot in self.crema_2compare.other_plots:
            self.fill_annex_plots(i_plot, self.crema_2compare.tour_sub_phase)

        self.report.print_summary_end()
        self.report.rst_to_html()

        # PDF report removed from version 0.5.6
        # if generate_pdf:
        #    self.report.rst2pdf(self.get_template_rst2pdf(orientation_landscape=report_orientation_landscape))

        if docx_template:
            docx_style_file = docx_template
        else:
            docx_style_file = self.get_template_docx()

        self.report.pandoc_html_to_docx(docx_style_file=docx_style_file)

        if new_report_name:
            self.report.rename_report(new_report_name, just_rename=True)

    def add_express_subsection(self):
        """
        Add a subsection with Radio source windows opportunities during flybys
        """

        self.report.write_head(3, 'Radio Source Parameters')

        message_no_radio_source = '\nNo radio Source subsection; input file provided (set "" in configuration file)\n'

        df_ref = self.crema_ref.expres_dataframes

        if df_ref is None:

            self.report.write_text(message_no_radio_source)

        else:

            self.report.write_text('\n This section provides time periods, as simulated by the ExPress tool, '
                                   'where JUICE is within +/- 12 hours around a moon CA flybys and '
                                   'when the targeted moon is occulting all Jupiter radio sources within frequency'
                                   ' range [9-11 MHz].flybys during which at least one of the Jupiter radio sources'
                                   ' is always visible from JUICE do not appear below.\n\n')

            self.report.write_head(3, 'Radio Source Parameters: Crema {}'.format(self.crema_ref.crema_id))
            my_tab = tabulate(df_ref, headers='keys', tablefmt='grid', numalign='center',
                              stralign='center',
                              showindex=False)

            self.report.write_text('\n' + my_tab + '\n')

        df = self.crema_2compare.expres_dataframes

        if df is None:

            logging.warning(message_no_radio_source)

        else:

            self.report.write_head(3, 'Radio Source Parameters: Crema {}'.format(
                self.crema_2compare.crema_id))
            my_tab = tabulate(df, headers='keys', tablefmt='grid', numalign='center',
                              stralign='center',
                              showindex=False)

            self.report.write_text('\n' + my_tab + '\n')

    def add_express_subsection_cmp(self):
        """
        Add a subsection with Radio source windows opportunities during flybys
        """

        df_ref = self.crema_ref.expres_dataframes

        if df_ref is None:

            self.report.write_text(
                '\n' + 'No radio Source subsection; input file provided (set "" in configuration file)' + '\n')

        else:

            self.report.write_head(3, 'Radio Source Parameters')

            self.report.write_text('\n This section provides time periods, as simulated by the ExPress tool, '
                                   'where JUICE is within +/- 12 hours around a moon CA flybys and '
                                   'when the targeted moon is occulting all Jupiter radio sources within frequency'
                                   ' range [9-11 MHz].flybys during which at least one of the Jupiter radio sources'
                                   ' is always visible from JUICE do not appear below.\n\n')

        df = self.crema_2compare.expres_dataframes

        if df is None:

            self.report.write_text('\n' + 'No comparison' + '\n')

        else:

            fb_ids = sorted(set(df_ref['Flyby'].tolist() + df['Flyby'].tolist()))

            ref_id = self.crema_ref.crema_id.split('_')[1]
            cmp_id = self.crema_2compare.crema_id.split('_')[1]

            headers = ['Flyby {}'.format(ref_id),
                       'Moon {}'.format(ref_id),
                       'Date CA {}'.format(ref_id),
                       'Radio Source occulted {}'.format(ref_id),
                       'sc altitudes [km] {}'.format(ref_id),
                       'Moon {}'.format(cmp_id),
                       'Date CA {}'.format(cmp_id),
                       'Radio Source occulted {}'.format(cmp_id),
                       'sc altitudes [km] {}'.format(cmp_id),
                       ]

            metric = []  # [headers]

            for fb in fb_ids:

                new_record = [fb]

                index_ref = df_ref.index[df_ref['Flyby'] == fb].tolist()

                if index_ref:

                    values = df_ref.loc[index_ref[0]].tolist()

                    new_record = new_record + [values[0]] + values[2:]

                else:

                    new_record = new_record + ['', '', '', '']

                index_cmp = df.index[df['Flyby'] == fb].tolist()

                if index_cmp:

                    values = df.loc[index_cmp[0]].tolist()
                    new_record = new_record + [values[0]] + values[2:]

                else:

                    new_record = new_record + ['', '', '', '']

                metric.append(new_record)

            metric = [[float(''.join(i for i in v[0] if i.isdigit()))] + v for v in metric]
            metric.sort()
            metric = [v[1:] for v in metric]

            my_tab = tabulate(metric, headers=headers, tablefmt='grid', numalign='center',
                              stralign='center',
                              showindex=False)

            self.report.write_text('\n' + my_tab + '\n')

    def fill_coverage_section(self):
        """
        Fill Coverage section
        """

        cov_ref = self.crema_ref.coverage_info
        cov_cmp = self.crema_2compare.coverage_info

        if cov_ref is None or cov_cmp is None:
            self.report.write_text(
                '\n' + 'No coverage_param metrics; input file provided (set "" in configuration file)' + '\n')
        else:

            for di in sorted(cov_ref.info.keys()):

                self.report.write_head(3, di.split('-')[1].capitalize())

                current_sub_dir = os.path.join(cov_ref.base_dir, di)
                current_sub_dir_cmp = os.path.join(cov_cmp.base_dir, di)

                self.report.write_head(4, self.crema_ref.crema_id)
                for f in sorted(cov_ref.info[di]):
                    self.add_coverage_plot(f, current_sub_dir)

                self.report.write_head(4, self.crema_2compare.crema_id)
                for f_cmp in sorted(cov_cmp.info[di]):
                    self.add_coverage_plot(f_cmp, current_sub_dir_cmp)

    def add_coverage_plot(self, f, current_sub_dir):
        """
        Add coverage plots

        :param f: coverage plot fiile path
        :param current_sub_dir: current sub_directory
        :return:
        """

        tmp_name = f.split('.')[0].split('__')
        id_trajectory = tmp_name[0]
        id_phase = tmp_name[1]
        id_parameter = tmp_name[2]
        if id_phase == "tour":
            id_target = str(tmp_name[3]).lower()
        else:
            id_target = os.path.basename(current_sub_dir).split('-')[1].lower()

        description = "Coverage of {} surface ({}) for crema_{}: {}.".format(
            id_target.capitalize(), id_phase, id_trajectory, id_parameter)

        title = '{} {}'.format(id_target.capitalize(), id_parameter.capitalize())
        coverage_plot = os.path.join(current_sub_dir, f)

        source = coverage_plot
        dst = os.path.join(self.plots_path, os.path.basename(coverage_plot))
        shutil.copy(source, dst)

        self.report.write_head(5, title)

        self.report.rst_insert_figure(dst, description, text="")

    def fill_eps_metric_section(self):
        """
        Report EPS metrics

        We are here going to reuse the soa_report python package to perform a JUICE's EPS simulation

        1) load eps_package info from json file or json data (dico)
           + run eps if requested (eps is run as part of set_up__from_json_file)

        2) get dataframe

        """

        ref_id = self.crema_ref.crema_id.replace('crema_', '')
        cmp_id = self.crema_2compare.crema_id.replace('crema_', '')
        dv_ref = self.crema_ref.eps_dataframes
        dv = self.crema_2compare.eps_dataframes

        if dv_ref is None:

            logging.warning('No EPS Metrics subsection; input file provided (set "EPS/OSVE" in configuration file)')
            self.report.write_text(
                '\n' + 'No EPS Metrics subsection; input file provided (set "EPS/OSVE" in configuration file)' + '\n')
        else:

            if dv is None:

                logging.warning('No DV!')

            else:

                #
                # TOTAL downlink Capacity
                #
                my_date_partitions = [self.crema_ref.reported_period_start, self.crema_ref.reported_period_end]
                data_frames_ref = self.get_periods(dv_ref, my_date_partition=my_date_partitions)
                my_date_partitions = [self.crema_2compare.reported_period_start,
                                      self.crema_2compare.reported_period_end]
                data_frames = self.get_periods(dv, my_date_partition=my_date_partitions)

                metrics_ref = self.report_summary_table(data_frames_ref)
                metrics = self.report_summary_table(data_frames)
                headers = ['Metric', f'Period Crema {ref_id}', f'Downlink {ref_id}\\n[Gbits]',
                           f'Period Crema {cmp_id}', f'Downlink {cmp_id}\\n[Gbits']

                merged_metrics = [headers] \
                                 + [[a[0], metrics_ref[0][1], str(a[1]), metrics[0][1], str(b[1])] for a, b in
                                    zip(metrics_ref[1:], metrics[1:])]

                # self.report.print_summary_sub_subsection(title='Downlink Capacity in Gbits for the Reported period',
                #                                          objective_summary=text, metrics=merged_metrics, figure=[])

                self.report.write_head(3, 'Downlink Capacity in Gbits')
                logging.info('Reporting Downlink Capacity in Gbits')
                self.report.print_rst_table_2(merged_metrics)

                #
                # Downlink Capacity in Gbits for the Tour
                #
                my_date_partitions = [self.crema_ref.tour_start, self.crema_ref.tour_end]
                data_frames_ref = self.get_periods(dv_ref, my_date_partition=my_date_partitions)
                my_date_partitions = [self.crema_2compare.tour_start, self.crema_2compare.tour_end]
                data_frames = self.get_periods(dv, my_date_partition=my_date_partitions)

                metrics_ref = self.report_summary_table(data_frames_ref)
                metrics = self.report_summary_table(data_frames)
                headers = ['Metric', f'Period Crema {ref_id}', f'Downlink {ref_id}\\n[Gbits]',
                           f'Period Crema {cmp_id}', f'Downlink {cmp_id}\\n[Gbits]']

                merged_metrics = [headers] \
                                 + [[a[0], metrics_ref[0][1], str(a[1]), metrics[0][1], str(b[1])] for a, b in
                                    zip(metrics_ref[1:], metrics[1:])]

                self.report.write_head(3, 'Downlink Capacity in Gbits for the Tour')
                logging.info('Reporting Downlink Capacity in Gbits for the Tour')
                self.report.print_rst_table_2(merged_metrics)
                # self.report_summary_table(data_frames, title='Generated DV, downlink, and SSM status in Gbits for the Tour')

                #
                # Downlink Capacity in Gbits for the Tour per sub-phase
                #
                metrics_ref = self.report_sub_phases_table_downlink_capacity(dv_ref, self.crema_ref.tour_sub_phase)
                metrics = self.report_sub_phases_table_downlink_capacity(dv, self.crema_2compare.tour_sub_phase)

                headers = ['Sub Phase', 'Description',
                           f'Period {ref_id}', f'Downlink {ref_id}\\n[Gbits]',
                           f'XB {ref_id}\\n[Gbits]', f'KA {ref_id}\\n[Gbits]',
                           f'Period {cmp_id}', f'Downlink {ref_id}\\n[Gbits]',
                           f'XB {ref_id}\\n[Gbits]', f'KA {ref_id}\\n[Gbits]']

                merged_metrics = [headers] \
                                 + [[a[0], a[-1]] + a[1:-1] + b[1:-1] for a, b in
                                    zip(metrics_ref[1:], metrics[1:])]

                self.report.write_head(3, 'Downlink Capacity [Gbits] per sub-phases for the Tour')
                logging.info('Reporting Downlink Capacity [Gbits] per sub-phases for the Tour')
                self.report.write_text('\n')

                self.report.print_rst_table_2(merged_metrics)

                # title='Downlink Capacity [Gbits] per sub-phases of Ganymede Phase')

                #
                # Downlink Capacity in Gbits for Ganymede Phase
                #
                my_date_partitions = [self.crema_ref.gco500_start, self.crema_ref.gco500_end]
                data_frames_ref = self.get_periods(dv_ref, my_date_partition=my_date_partitions)
                my_date_partitions = [self.crema_2compare.gco500_start, self.crema_2compare.gco500_end]
                data_frames = self.get_periods(dv, my_date_partition=my_date_partitions)

                metrics_ref = self.report_summary_table(data_frames_ref)
                metrics = self.report_summary_table(data_frames)
                headers = ['Metric', f'Period Crema {ref_id}', f'Dowlnlink {ref_id}\\n[Gbits]',
                           f'Period Crema {cmp_id}', f'Dowlnlink {cmp_id}\\n[Gbits]']
                self.report.write_head(3, 'Downlink Capacity in Gbits for Ganymede Phase')
                logging.info('Reporting Downlink Capacity in Gbits for Ganymede Phase')
                self.report.write_text('\n')

                message_no_data = 'There is no data for Crema {}!'

                n_metrics_ref = len(metrics_ref[0])
                n_metrics = len(metrics[0])

                if n_metrics_ref > 1 and n_metrics > 1:

                    merged_metrics = [headers] \
                                     + [[a[0], metrics_ref[0][1], str(a[1]), metrics[0][1], str(b[1])] for a, b in
                                        zip(metrics_ref[1:], metrics[1:])]

                    self.report.print_rst_table_2(merged_metrics)

                elif n_metrics <= 1 and n_metrics_ref <= 1:

                    logging.warning(message_no_data.format(ref_id))
                    self.report.write_text(message_no_data.format(ref_id))
                    logging.warning(message_no_data.format(cmp_id))
                    self.report.write_text(message_no_data.format(cmp_id))

                elif n_metrics_ref <= 1:

                    logging.warning(message_no_data.format(ref_id))
                    self.report.write_text(message_no_data.format(ref_id))

                    single_metrics = [['Metric', 'Period Crema {}'.format(cmp_id), 'DV {}\\n[Gbits]'.format(
                        cmp_id)], [metrics[1][0], metrics[0][1], metrics[1][1]]]

                    self.report.print_rst_table_2(single_metrics)

                elif n_metrics <= 1:

                    logging.warning(message_no_data.format(cmp_id))
                    self.report.write_text(message_no_data.format(cmp_id))

                    single_metrics = [['Metric', 'Period Crema {}'.format(ref_id), 'DV {}\\n[Gbits]'.format(
                        ref_id)], [metrics_ref[1][0], metrics_ref[0][1], metrics_ref[1][1]]]

                    self.report.print_rst_table_2(single_metrics)

                self.report.write_head(3, 'Downlink Capacity [Gbits] per sub-phases of Ganymede Phase')
                metrics_ref = self.report_sub_phases_table_downlink_capacity(dv_ref, self.crema_ref.ganymede_sub_phase)
                metrics = self.report_sub_phases_table_downlink_capacity(dv, self.crema_2compare.ganymede_sub_phase)

                headers = ['Sub Phase', 'Description',
                           'Period {}'.format(ref_id), 'Downlink {}\\n[Gbits]'.format(ref_id),
                           'XB {}\\n[Gbits]'.format(ref_id), 'KA {}\\n[Gbits]'.format(ref_id),
                           'Period {}'.format(cmp_id), 'Downlink {}\\n[Gbits]'.format(ref_id),
                           'XB {}\\n[Gbits]'.format(ref_id), 'KA {}\\n[Gbits]'.format(ref_id)]

                merged_metrics = [headers] \
                                 + [[a[0], a[-1]] + a[1:-1] + b[1:-1] for a, b in
                                    zip(metrics_ref[1:], metrics[1:])]

                self.report.write_text('\n')
                self.report.print_rst_table_2(merged_metrics)

                # merged_metrics = self.report_summary_table(data_frames)
                # self.report.print_summary_sub_subsection(title='Downlink Capacity [Gbits] per sub-phases of Ganymede Phase',
                #                                          objective_summary=text, metrics=merged_metrics, figure=[])
                #
                # #, title='Downlink Capacity in Gbits for the Ganymede phase')
                #
                # self.report_sub_phases_table_dowlink_capacity(dv, self.crema_ref.ganymede_sub_phase,
                #                                               title='Downlink Capacity [Gbits] per sub-phases of Ganymede Phase')

    def fill_annex_ground_station_plots(self, gs_plots):
        """
        Report Ground Stations elevation and Visibility Limit plots

        :param gs_plots: Ground Stations elevation and Visibility Limit plots
        """

        if os.path.exists(gs_plots):

            self.report.write_head_subsubsection('Ground Stations elevation and Visibility Limit ')

            self.report.write_text('\n\nThis subsection contains Ground Stations elevation and'
                                   ' visibility limit for each flyby of the Tour\n\n')

            list_of_plots = os.listdir(gs_plots)

            to_sort = []

            for f in list_of_plots:
                flyby_index = f.replace('.png', '').replace('Flyby_stations_elevation_', '')
                f_index = float(''.join([c for c in flyby_index if c.isnumeric()]))
                to_sort.append([f_index, flyby_index, f])

            sorted_list = sorted(to_sort)

            for [f_index, flyby_index, f] in sorted_list:
                fi = os.path.join(gs_plots, f)
                fi_title = 'Ground Stations elevation and Visibility Limit: {}\n'.format(flyby_index)
                fig = os.path.expandvars(fi)
                # self.report.print_summary_sub_subsection(fi_title, figure=[fig])
                self.report.rst_insert_figure(fig, text='', title=fi_title)

            logging.info('Plot directory processed {}'.format(gs_plots))

        else:

            logging.warning('Plot directory does not exits: {}'.format(gs_plots))

    def fill_annex_plots(self, plot_dir, tour_sub_phase=None):
        """
        Report more plots within ANNEX section from directory

        :param tour_sub_phase: list of ordered mission sub-phases (Tour)
        :param plot_dir: directory where plot are located
        """

        if os.path.exists(plot_dir):

            base_name = (os.path.basename(plot_dir)).replace('_', ' ').capitalize()

            self.report.write_head(3, base_name)

            list_of_plots = os.listdir(plot_dir)

            # check if txt and/or csv file in list_of_plots:
            list_of_txt_files = [f for f in list_of_plots if f.endswith(".txt")]
            list_of_csv_files = [f for f in list_of_plots if f.endswith(".csv")]
            list_of_plots = [f for f in list_of_plots if f.endswith(".png")]

            self.write_txt_file_in_report(list_of_txt_files, plot_dir)

            for f_csv in sorted(list_of_csv_files):
                fi = open(os.path.join(plot_dir, f_csv), 'r')
                df = pd.read_csv(fi, sep=";", comment='#')
                my_tab = tabulate(df, headers='keys', tablefmt='grid', numalign='center',
                                  stralign='center',
                                  showindex=False)

                self.report.write_text('\n' + my_tab + '\n')
                fi.close()

            sub_phase_label_to_index = {}
            nb_tour_sub_phase = len(tour_sub_phase)

            for i in range(nb_tour_sub_phase):
                i_label = tour_sub_phase[i].description.replace(' ', '').lower()
                sub_phase_label_to_index[i_label] = i

            new_list_of_plots = []

            for f in list_of_plots:

                fi_title = (os.path.basename(f)).replace('.png', '')
                sub_phase_label = fi_title.split('_comparisons_')[1].lower()
                if sub_phase_label not in list(sub_phase_label_to_index.keys()) is None:
                    index_sub_phase_label = nb_tour_sub_phase + 10  # bigger than nb+1 => low priority
                else:
                    index_sub_phase_label = sub_phase_label_to_index[sub_phase_label]
                fi = os.path.join(plot_dir, f)
                fi_title = '{}\n'.format(fi_title)
                fig = os.path.expandvars(fi)
                new_list_of_plots.append([index_sub_phase_label, sub_phase_label, fi_title, fig])

            new_list_of_plots = sorted(new_list_of_plots, key=itemgetter(0, 2))

            for [ind, label, fi_title, fig] in new_list_of_plots:
                self.report.rst_insert_figure(fig, text='', title=fi_title)

            logging.info('Plot directory processed {}'.format(plot_dir))

        else:

            logging.warning('Plot directory does not exits: {}'.format(plot_dir))

    def add_perijove_flyby_details(self, crema):
        """
        Add details on Fluby and Perojove

        :param: crema objects (structure)
        """

        self.report.write_head(3, 'Perijove Geometry Summary ({})'.format(crema.crema_id))
        self.report.write_text("\n")

        if crema.perijove_details:
            self.report.print_rst_table_2(crema.perijove_details)
        else:
            self.report.write_text("\nNo perijove data provided as input\n")

        self.report.write_head(3, 'Flybys Geometry Summary ({})'.format(crema.crema_id))
        self.report.write_text("\n")

        if crema.flyby_details:
            self.report.print_rst_table_2(crema.flyby_details)
        else:
            self.report.write_text("\nNo flyby data provided as input\n")

    def add_cruise_flyby_details(self, crema):
        """
        Add details on Cruise Flybys

        :param: crema objects (structure)
        """

        self.report.write_head(3, 'Cruise Flybys Summary {}'.format(crema.crema_id))
        self.report.write_text("\n")

        if crema.cruise_details:
            self.report.write_text("Method used to identify cruise flybys:\n"
                                   "Currently the geopipeline identifies the cruise flybys by searching for local minimum "
                                   "(altitude < 20000 km).\n")
            self.report.print_rst_table_2(crema.cruise_details)
        else:
            self.report.write_text("\nNo data provided as input\n")

    def get_template_rst2pdf(self, orientation_landscape=False):
        """
        Get the rst2pdf.style template hosted in source code within templates sub-directory

        :param: orientation_landscape: Flag to enforce A4 landscape orientation; default False
        :return: rst2pdf.style  path
        :rtype: python path
        """

        default_template = 'default_rst2pdf.style'
        if orientation_landscape:
            default_template = 'default_a4_landscape_rst2pdf.style'

        here = os.path.abspath(os.path.dirname(__file__))
        template_file = os.path.join(here, 'templates')
        template_file = os.path.join(template_file, default_template)

        if not os.path.exists(template_file):
            logging.error('reference template file "%s" missing' % template_file)
            sys.exit()

        logging.info('{} loaded'.format(template_file))

        return template_file

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

    def set_up_parameters(self, root_path, output_dir=''):
        """
        Set up parameters

        :param root_path: base directory of scenario
        :param output_dir: path of output directory (there is a default values)
        :return: scenario, root_path, output_dir, plots_path
        """

        if output_dir == '':
            output_dir = os.path.join(root_path, 'traject_output')
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)
        else:
            output_dir = os.path.expandvars(output_dir)
            if not os.path.exists(output_dir):
                logging.warning('output dir does not exist: {}'.format(output_dir))
                output_base_dir = os.path.dirname(output_dir)

                if os.path.exists(output_base_dir):
                    logging.warning('output base directory exist; Trying to create output dir: {}'.format(output_dir))
                    os.mkdir(output_dir)

                else:

                    logging.error('Output dir nor output base directory exist')
                    logging.error(f'Please check output_dir in config file: {output_dir}')
                    sys.exit()

        plots_path = os.path.join(output_dir, 'plots')
        if not os.path.exists(plots_path):
            os.mkdir(plots_path)

        return root_path, output_dir, plots_path

    def write_txt_file_in_report(self, list_of_txt_files, plot_dir):
        """
        Write txt file as is in report

        :param list_of_txt_files: list of txt files
        :param plot_dir: plot directory
        """

        for f_txt in list_of_txt_files:

            fi = open(os.path.join(plot_dir, f_txt), 'r')
            self.report.write_text('\n')
            for line in fi.readlines():
                if line.startswith('....'):
                    line = '\n'
                self.report.write_text(line)

            self.report.write_text('\n')
            fi.close()

