"""
Created on July, 2020

@author: Claudio Munoz Crego (ESAC)

This Module allows to report trajectory assessment subsection including plots
"""

import os
import shutil
import sys
import datetime
import logging
import numpy as np

from juice_trajectory_assessment.report.rst_report import RstReport
from soa_report.juice.eps_data.df_data_rate_avg import DfDataRateAverage


class BasicReport(object):
    """
    This class allows to report trajectory assessment using SOC simulation Metrics
    """

    def __init__(self, start=None, end=None, output_dir='./'):

        self.output_dir = output_dir
        self.plots_path = None

        (self.start, self.end) = (start, end)

        self.report = None

    def report_sub_phases_table_dowlink_capacity(self, dv, sub_phases,
                                                 title='Downlink Capacity [Gbits] per sub-phases', ):
        """
        Create a table including Downlink Capacity in Gbits for each sub-phase

        Notes:
        - The sum of all (sub-periods) in included in a an additional (last) column if the number of sub-periods > 1.
        - The table is transposed (rows <-> lines) if number of sub-periods > 3 for user readability.

        :param dv: dictionary including a subset of dataframes; keys are labels <start>_<end>
        :param sub_phases: dictionary including the list of sub-phases ordered by time
        :param title: Table title
        """

        dfs_all = dv
        simulation_start = dfs_all.start
        simulation_end = dfs_all.end

        sub_phases_header = ['sub-phase', 'period', 'Total [Gbits]', 'XB [Gbits]', 'KA [Gbits]', 'Description']
        metrics = [sub_phases_header]

        for sp in sub_phases:

            # print(sp.id, sp.start, sp.end)

            if sp.end < simulation_start or sp.start > simulation_end:

                period = "{} {}".format(sp.start, sp.end)

                metrics.append([sp.id, period, '0', '0', '0', sp.description])

            else:

                my_date_partitions = [sp.start, sp.end]
                dfs = self.get_periods(dv, my_date_partition=my_date_partitions)

                periods = [s.replace('_', ' ') for s in sorted(dfs.keys())]
                periods = [s.replace('T', ' ') for s in periods]

                if not dfs:
                    logging.info(f'There are no data for the period [{sp.start} - {sp.end}]')
                    self.report.write(f'There are no data for the period [{sp.start} - {sp.end}]')

                values_total = [round(dfs[k].get_total_downlink(), 2) for k in sorted(dfs.keys())]
                values_x = [round(dfs[k].get_total_downlink('XB_LINK'), 2) for k in sorted(dfs.keys())]
                values_ka = [round(dfs[k].get_total_downlink('KAB_LINK'), 2) for k in sorted(dfs.keys())]
                metrics.append([sp.id] + periods + values_total + values_x + values_ka + [sp.description])

        self.report.print_table(title, metrics)

    def report_sub_phases_table_generated_dv(self, dv, sub_phases, title='Generated DV [Gbits] per sub-phases'):
        """
        Create a table including generated DV in Gbits for each sub-phase

        Notes:
        - The sum of all (sub-periods) in included in a an additional (last) column if the number of sub-periods > 1.
        - The table is transposed (rows <-> lines) if number of sub-periods > 3 for user readability.

        :param dv: dictionary including a subset of dataframes; keys are labels <start>_<end>
        :param sub_phases: dictionary including the list of sub-phases ordered by time
        :param title: Table title
        """

        dfs_all = dv
        simulation_start = dfs_all.start
        simulation_end = dfs_all.end

        sub_phases_header = ['sub-phase', 'period', 'Generated DV [Gbits]', 'Description']
        metrics = [sub_phases_header]

        for sp in sub_phases:

            if sp.end < simulation_start or sp.start > simulation_end:

                period = "{} {}".format(sp.start, sp.end)

                metrics.append([sp.id, period, '0', sp.description])

            else:

                my_date_partitions = [sp.start, sp.end]
                dfs = self.get_periods(dv, my_date_partition=my_date_partitions)

                periods = [s.replace('_', ' ') for s in sorted(dfs.keys())]
                periods = [s.replace('T', ' ') for s in periods]

                if not dfs:
                    logging.info('There are no data for the period [{} - {}]'.format(sp.start, sp.end))
                    self.report.write('There are no data for the period [{} - {}]'.format(sp.start, sp.end))

                values = [round(sum(dfs[k].get_total_accum_data_volume().values()), 2) for k in sorted(dfs.keys())]
                metrics.append([sp.id] + periods + values + [sp.description])

        self.report.print_table(title, metrics)

    def report_summary_table(self, dfs, title='Generated DV, downlink, and SSM status in Gbits',
                             generated_dv=False, downlink_capacity=True, total_downlink=False, text=''):
        """
        Create a summary report including for all sub-periods:

        - Generated data Volume (total)
        - Total Downlink Data Volume capability
        - Actual Total Downlink Data Volume to ground
        - data in the SSMM at the beginning of scenario
        - Remaining data in the SSMM at the end of scenario

        Notes:
        - The sum of all (sub-periods) in included in a an additional (last) column if the number of sub-periods > 1.
        - The table is transposed (rows <-> lines) if number of sub-periods > 3 for user readability.

        :param title: Table title
        :param dfs: dictionary including a subset of dataframes; keys are labels <start>_<end>
        :param generated_dv: flag to indicate Generated data Volume must be report
        :param downlink_capacity: flag to indicate downlink capacity must be report
        :param total_downlink: flag to indicate total_downlink to ground must be report
        """

        periods = [s.replace('_', ' ') for s in sorted(dfs.keys())]
        periods = [s.replace('T', ' ') for s in periods]
        sub_phases_header = ['Metric'] + periods + ['Total']
        metrics = [sub_phases_header]
        if generated_dv:
            values = [round(sum(dfs[k].get_total_accum_data_volume().values()), 2) for k in sorted(dfs.keys())]
            metrics.append(['Generated data Volume (total)'] + values + [sum(values)])
        if downlink_capacity:
            values = [round(dfs[k].get_total_downlink(), 2) for k in sorted(dfs.keys())]
            metrics.append(['Total Downlink Data Volume capability'] + values + [sum(values)])
            values = [round(dfs[k].get_total_downlink('XB_LINK'), 2) for k in sorted(dfs.keys())]
            metrics.append(['Total Downlink Data Volume capability XB_LINK'] + values + [sum(values)])
            values = [round(dfs[k].get_total_downlink('KAB_LINK'), 2) for k in sorted(dfs.keys())]
            metrics.append(['Total Downlink Data Volume capability KAB_LINK'] + values + [sum(values)])
        if total_downlink:
            values = [round(dfs[k].get_total_ssmm_accum(), 2) for k in sorted(dfs.keys())]
            metrics.append(['Actual Total Downlink Data Volume to ground'] + values + [sum(values)])
            values = [round(dfs[k].get_x_band_accum(), 2) for k in sorted(dfs.keys())]
            metrics.append(['Actual Total Downlink Data Volume to ground XB_LINK'] + values + [sum(values)])
            values = [round(dfs[k].get_ka_band_accum(), 2) for k in sorted(dfs.keys())]
            metrics.append(['Actual Total Downlink Data Volume to ground KAB_LINK'] + values + [sum(values)])
            values = [round(dfs[k].get_ssmm_initial_value(), 2) for k in sorted(dfs.keys())]
            if len(values) == 0:
                init_val = 0
            else:
                init_val = values[0]
            metrics.append(['data in the SSMM at the beginning of scenario'] + values + [init_val])
            values = [round(dfs[k].get_ssmm_last_value(), 2) for k in sorted(dfs.keys())]
            if len(values) == 0:
                remaining_data = 0
            else:
                remaining_data = values[-1]
            metrics.append(['Remaining data in the SSMM at the end of scenario'] + values + [remaining_data])

        if len(dfs) <= 1:
            metrics = [row[:-1] for row in metrics]

        if len(dfs.keys()) > 3:
            metrics = np.array(metrics).T.tolist()

        if not periods:
            metrics = []

        self.report.print_summary_subsection(title, objective_summary=text, metrics=metrics, figure=[])

    def get_periods(self, dv, df_type=DfDataRateAverage, my_date_partition=None):
        """
        Defines data_frames subset

        :param dv: pandas dataframe for the whole scenario
        :return: list of pandas dataframe corresponding to a given subset if periods
        """

        if my_date_partition is None:
            my_date_partition = self.my_date_partition

        date_format = '%Y-%m-%dT%H:%M:%S.%f'
        dv_time_step = (dv.df['datetime (UTC)'][1] - dv.df['datetime (UTC)'][0]).total_seconds()

        data_frames = {}
        for i in range(len(my_date_partition) - 1):

            (start, end) = (my_date_partition[i], my_date_partition[i + 1])
            start_str = datetime.datetime.strftime(start, date_format).split('.')[0]
            end_str = datetime.datetime.strftime(end, date_format).split('.')[0]
            period_label = '{}_{}'.format(start_str, end_str)

            if (end - start).total_seconds() > dv_time_step:

                if start > dv.end or end < dv.start:
                    logging.warning('Periods {} avoided; No data in data_avg_file.out define in period [{} - {}] '
                                    'for requested period [{}: {}]'.format(period_label, dv.start, dv.end, start, end))
                    logging.warning('Please check the eps_package against Mission_phase')

                else:

                    new_df = df_type(dv.df, start, end)
                    data_frames[period_label] = new_df
            else:
                logging.warning('Periods {} avoided; too short < {} sec'.format(
                    period_label, (end - start).total_seconds()))

        return data_frames
