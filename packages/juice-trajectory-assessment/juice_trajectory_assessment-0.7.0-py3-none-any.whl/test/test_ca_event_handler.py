"""
Created on September, 2020

@author: Claudio Munoz Crego (ESAC)

This Module allows to handle (parse, load) CA event files
"""

import os
import logging
import numpy as np

import sys
import pandas as pd
import datetime

from tabulate import tabulate

from juice_trajectory_assessment.commons.ca_event_handler import EventCaHandler, find_index_closest_date
from juice_trajectory_assessment.commons.ca_event_handler import read_file


def get_rime_opp(segment_file):

    print(segment_file)

    df_express_seg = read_file(segment_file, header=None, col_names=['event', 'start UTC', 'end UTC', 'x', 'wg'])

    #
    # my_tab = tabulate(df_express_seg[:10], headers='keys', tablefmt='grid', numalign='center', stralign='center',
    #                   showindex=False)
    # print('\n' + my_tab + '\n')

    df_exp = df_express_seg.loc[df_express_seg['event'].str.contains('RIME_AJS')]

    # my_tab = tabulate(df_exp[:10], headers='keys', tablefmt='grid', numalign='center', stralign='center', showindex=False)
    # print('\n' + my_tab + '\n')

    df_moon = p.get_moon_flyby()

    rime_ajs = {'GANYMEDE_FLYBY_RIME_AJS': '',
                'CALLISTO_FLYBY_RIME_AJS': '',
                'EUROPA_FLYBY_RIME_AJS': ''}
    for i in range(len(df_exp['event'].tolist())):

        event = df_exp['event'].iloc[i]
        start = df_exp['start UTC'].iloc[i][:-1]
        end = df_exp['end UTC'].iloc[i][:-1]
        dt = datetime.datetime.strptime(df_exp['start UTC'].iloc[i], '%Y-%m-%dT%H:%M:%SZ')

        df = find_index_closest_date(df_moon, 'datetime (UTC)', dt)
        # print('\ninput date: {} --> CA or sub_phase is {} [{}] '.format(
        #     dt, df['Event name'], str(df['datetime (UTC)']).split('.')[0]))
        if 'PJ' not in df['Event name']:

            if rime_ajs[event] == '':
                rime_ajs[event] = '[{}]:[{}, {}]'.format(df['Event name'], start, end)
            else:
                rime_ajs[event] = rime_ajs[event] + '\n[{}]:[{}, {}]'.format(df['Event name'], start, end)

    my_tab = tabulate(rime_ajs.items(), headers=['Parameters', 'Values'], tablefmt='grid', numalign='center',
                      stralign='center',
                      showindex=False)
    print('\n' + my_tab + '\n')


if __name__ == '__main__':

    from esac_juice_pyutils.commons.my_log import setup_logger

    here = os.path.abspath(os.path.dirname(__file__))
    test_dir = os.path.dirname(here)

    setup_logger()

    logging.info('here: {}'.format(here))
    print(test_dir)

    setup_logger('Start Test')

    input_file = '../TDS/conf/crema_3.0/mission_timeline_event_file_3_0-short.csv'

    p = EventCaHandler(input_file)

    df = p.get_moon_flyby('Callisto')
    print(df)

    dt_str = '2030-09-20T18:07:20'
    dt = datetime.datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S')

    print(df.keys())
    df = find_index_closest_date(df, 'datetime (UTC)', dt)

    print('\ninput date: {} --> CA or sub_phase is {}'.format(dt_str, df['Event name']))

    dt_str = '2030-09-23T18:07:20'
    dt = datetime.datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S')
    df = p.get_moon_flyby()
    df = find_index_closest_date(df, 'datetime (UTC)', dt)
    # print('\ninput date: {} --> CA or sub_phase is {} [{}] '.format(
    #     dt_str, df['Event name'], str(df['datetime (UTC)']).split('.')[0]))

    segment_file = '../TDS/JIRA_TEST/JSA-295/input/expres_derived_segments_opportunities_3.0.csv'
    get_rime_opp(segment_file)

    # df_express_seg = read_file(segment_file, header=None, col_names=['event', 'start UTC', 'end UTC', 'x', 'wg'])
    #
    # #
    # my_tab = tabulate(df_express_seg[:10], headers='keys', tablefmt='grid', numalign='center', stralign='center', showindex=False)
    # print('\n' + my_tab + '\n')
    #
    # df_exp = df_express_seg.loc[df_express_seg['event'].str.contains('RIME_AJS')]
    #
    # my_tab = tabulate(df_exp[:10], headers='keys', tablefmt='grid', numalign='center', stralign='center', showindex=False)
    # print('\n' + my_tab + '\n')
    #
    # df_moon = p.get_moon_flyby()
    #
    # rime_ajs = {'GANYMEDE_FLYBY_RIME_AJS': '',
    #             'CALLISTO_FLYBY_RIME_AJS': '',
    #             'EUROPA_FLYBY_RIME_AJS': ''}
    # for i in range(len(df_exp['event'].tolist())):
    #
    #     event = df_exp['event'].iloc[i]
    #     start = df_exp['start UTC'].iloc[i][:-1]
    #     end = df_exp['end UTC'].iloc[i][:-1]
    #     dt = datetime.datetime.strptime(df_exp['start UTC'].iloc[i], '%Y-%m-%dT%H:%M:%SZ')
    #
    #     df = find_index_closest_date(df_moon, 'datetime (UTC)', dt)
    #     # print('\ninput date: {} --> CA or sub_phase is {} [{}] '.format(
    #     #     dt, df['Event name'], str(df['datetime (UTC)']).split('.')[0]))
    #     if 'PJ' not in df['Event name']:
    #
    #         if rime_ajs[event] == '':
    #             rime_ajs[event] = '[{}]:[{}, {}]'.format(df['Event name'], start, end)
    #         else:
    #             rime_ajs[event] = rime_ajs[event] + '\n[{}]:[{}, {}]'.format(df['Event name'], start, end)
    #
    # my_tab = tabulate(rime_ajs.items(), headers=['Parameters', 'Values'], tablefmt='grid', numalign='center', stralign='center',
    #                       showindex=False)
    # print('\n' + my_tab + '\n')

    segment_file = '../TDS/JIRA_TEST/JSA-295/input/expres_derived_segments_opportunities_3_2.csv'
    get_rime_opp(segment_file)

    logging.debug('End of test')
