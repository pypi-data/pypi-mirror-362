"""
Created on October, 2020

@author: Claudio Munoz Crego (ESAC)

This Module allows to handle (parse, load) Juice mission timeline Event files
"""


import os
import sys
import logging
import datetime
import pandas as pd
import copy
from tabulate import tabulate


class MissionTimelineEvent(object):
    """
    Juice mission timeline Event File Handler
    """

    def __init__(self, file_input, output_dir="./"):

        self.output_dir = output_dir

        self.input_file = file_input

        self.df = self.read_event_timeline_file()

    def read_event_timeline_file(self):
        """
        Read Juice mission timeline Event File
        :return: df
        """

        col_names = ['Event name', 'event time [utc]', 'contextual info']

        df = read_file(self.input_file, header=None, col_names=col_names)

        if df.iloc[0, 0].startswith('Event name'):
            df.iloc[0, 0] = '#' + df.iloc[0, 0]

        df['datetime (UTC)'] = pd.to_datetime(df['event time [utc]'], format="%Y-%m-%dT%H:%M:%SZ", errors='coerce')
        df['datetime (UTC)'] = df['event time [utc]']
        df = df.drop(columns=['event time [utc]'])

        return df

    def get_flyby_and_PE_events(self, output_format='dico'):
        """
        Get Flyby and PErijove sub_phases from mission timeline event file

        :return: my_events: dictionary {Flyby and PErijove} vs datetime
        """

        df2 = self.df[self.df['Event name'].str.startswith('FLYBY_') | self.df['Event name'].str.startswith('PERIJOVE_')]

        my_events = {}
        my_dico = {'Event name': [], 'event time [utc]': [], 'datetime (UTC)': []}
        for i in range(len(df2)):

            id = df2.iloc[i]['Event name']
            dt = df2.iloc[i]['datetime (UTC)']
            other = df2.iloc[i]['contextual info']

            if id.startswith('PERIJOVE_'):

                event_name = id.replace('PJ', '').replace('PERIJOVE_', 'PJ')
                ca_time = 'None'
                ca_alt = 'None'

            elif id.startswith('FLYBY_'):

                event_name = other.split(';')[0].split()[-1]

                ca_time = other.split(';')[1].replace(' ', '')
                ca_time = ca_time[5:]  # Remove Time? at the beginning to get date
                ca_alt = other.split(';')[2].replace(' ', '')
                ca_alt = ca_alt.split('=')[1]

                ca_time = datetime.datetime.strptime(ca_time, '%d-%b-%Y_%H:%M:%S')
                ca_time = datetime.datetime.strftime(ca_time, '%Y-%m-%dT%H:%M:%S')

            event_date = datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M:%SZ')

            my_events[event_date] = event_name

            my_dico['Event name'].append(event_name)
            my_dico['event time [utc]'].append(ca_time)
            my_dico['datetime (UTC)'].append(event_date)

        if output_format == 'dataframe':
            my_events = pd.DataFrame(my_dico)

        return my_events

    def get_flyby_events_details(self):
        """
        Get Flyby from mission timeline event file

        :return: my_events: dictionary {Flyby} vs datetime
        """

        df2 = self.df[self.df['Event name'].str.startswith('FLYBY_')]

        my_events = []

        for i in range(len(df2)):

            my_dico = {}

            dt = df2.iloc[i]['datetime (UTC)']
            other = df2.iloc[i]['contextual info']

            event_name = other.split(';')[0].split()[-1]

            ca_time = other.split(';')[1].replace(' ', '')
            ca_time = ca_time[5:]  # Remove Time? at the beginning to get date

            ca_time = datetime.datetime.strptime(ca_time, '%d-%b-%Y_%H:%M:%S')
            ca_time = datetime.datetime.strftime(ca_time, '%Y-%m-%dT%H:%M:%S')

            my_dico['Event name'] = event_name
            my_dico['event time [UTC]'] = ca_time

            for col in other.split(';')[2:]:

                col_name, value = col.split('=')

                value = value.lstrip()

                if value.startswith('*'):
                    value = '\\' + value

                my_dico[col_name] = value

            my_events.append(my_dico)

        return my_events

    def get_perijove_events_details(self):
        """
        Get PErijove sub_phases from mission timeline event file

        :return: my_events: dictionary {PERIJOVE} vs datetime
        """

        df2 = self.df[self.df['Event name'].str.startswith('PERIJOVE_')]

        my_events = []

        for i in range(len(df2)):

            my_dico = {}
            id = df2.iloc[i]['Event name']
            other = df2.iloc[i]['contextual info']

            event_name = id.replace('PJ', '').replace('PERIJOVE_', 'PJ')

            my_dico['Event name'] = event_name

            for col in  other.split(';')[1:]:

                col_name, value = col.split('=')

                value = value.lstrip()

                if value.startswith('*'):
                    value = '\\' + value

                my_dico[col_name] = value

            my_events.append(my_dico)

        return my_events

    def get_sun_conjunctions(self, as_dico=True):
        """
        Get SUN_CONJUNCTION from mission timeline event file

        :return: return list of Sun Conjunctions periods
        """

        df2 = self.df[self.df['Event name'].str.startswith('SUN_CONJUNCTION_SUP')]

        my_tab = tabulate(df2, headers='keys', tablefmt='grid', numalign='center',
                          stralign='center',
                          showindex=False)

        print('\n' + my_tab + '\n')

        sun_conjunctions_periods = []

        start = datetime.datetime.strptime(df2.iloc[0]['datetime (UTC)'], '%Y-%m-%dT%H:%M:%SZ')
        end = datetime.datetime.strptime(df2.iloc[-1]['datetime (UTC)'], '%Y-%m-%dT%H:%M:%SZ')

        for i in range(len(df2)):

            id = df2.iloc[i]['Event name']
            dt = df2.iloc[i]['datetime (UTC)']
            dt = datetime.datetime.strptime(dt, '%Y-%m-%dT%H:%M:%SZ')

            if id.endswith('_START'):
                start = dt
            elif id.endswith('_END'):
                sun_conjunctions_periods.append([start, dt])

        # Check last conjunction ends; if not extend it until end
        if id.endswith('_START'):
            sun_conjunctions_periods.append([start, end])

        if as_dico:

            return {'SUN_CONJUNCTION_SUP': sun_conjunctions_periods}

        else:

            return sun_conjunctions_periods


def read_file(input_file, header=[0], sep=',', col_names=None):
    """
    Read csv like file

    :param header: specify header lines; default is None
    :param input_file: path of the csv file to read
    :param sep: cvs file separator (i.e, ",")
    :param col_names: list of column names; Defualt is None
    :return: df: panda data frame instance containing input data
    """

    if not os.path.exists(input_file):
        logging.error('input file "{}" not available'.format(input_file))
        sys.exit()  # event line output routine
    else:

        if col_names:

            df = pd.read_csv(input_file, sep=sep, header=None, comment='#', names=col_names)

        else:

            df = pd.read_csv(input_file, sep=sep, header=header, comment='#')

    return df






