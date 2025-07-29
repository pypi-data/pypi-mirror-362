"""
Created on July, 2020

@author: Claudio Munoz Crego (ESAC)

This Module allows to handle (parse, load) mission phase files
"""

import logging
import os

import sys
import pandas as pd
import datetime


class MissionPhaseHandler(object):
    """
    This Class allows read and parse Juice Mission Phase
    """

    def __init__(self, file_input, output_dir="./"):

        self.output_dir = output_dir

        self.input_file = file_input

        self.mission_phases = self.get_mission_phases()
        self.print_mission_phases()

    def get_mission_phases(self):
        """
        Read Working mission_phase file

        1) parse csv file

        :return: mission_phases
        """

        df = self.read_file(self.input_file, sep=',')

        mission_phases = {}

        for i in range(len(df)):
            row = df.iloc[i]
            label = str(row.iloc[0]).upper()
            description = str(row.iloc[1])
            start = self.parse_date_time(str(row.iloc[2]).strip())
            end = self.parse_date_time(str(row.iloc[3]).strip())

            mission_phases[label] = MissionPhase(label, str(description).lstrip(), start, end)

        return mission_phases

    def print_mission_phases(self):
        """
        Print mission phases in stdout
        :return:
        """
        logging.info('Juice Mission Phases')
        for m in self.mission_phases.keys():

            print('\t{}'.format(self.mission_phases[m].to_string()))

    def parse_date_time(self, str_date):
        """
        Parse date time

        :param str_date: date time provided a a string
        :return:
        """
        """
        Parse Mission phases period date time format to datetime object
    
        1) Try some specific format first
        2) use datetutils wich support most common formats
        :return:
        """

        from dateutil.parser import parse

        datetime_formats = ['%d-%b-%Y_%H:%M:%S',
                            '%d-%B-%Y_%H:%M:%S',
                            '%d/%m/%y',
                            '%Y-%m-%dT%H:%M:%SZ',
                            '%Y-%m-%d %H:%M:%S']

        dt = None

        for dt_format in datetime_formats:

            try:

                dt = datetime.datetime.strptime(str_date, dt_format)

                if dt:
                    break

            except IOError as e:
                logging.debug(("I/O error({0}): {1}".format(e.errno, e.strerror)))

            except ValueError:
                logging.debug('Bad date time format "{}"; Expected format is "{}"'.format(
                    str_date, datetime.datetime.strftime(datetime.datetime.now(), dt_format)))

        try:

            if dt is None:
                dt = parse(str_date)

        except IOError as e:
            logging.debug(("I/O error({0}): {1}".format(e.errno, e.strerror)))

        except ValueError:
            logging.debug('Bad date time format "{}"; Expected format is "{}"'.format(
                str_date, datetime.datetime.strftime(datetime.datetime.now(), dt_format)))

        if dt is None:
            logging.error('Cannot parse "{}" to datetime format!'.format(str_date))
            sys.exit()

        return dt

    def read_file(self, input_file, header=[0], sep=','):
        """
        Read csv like file

        :param sep:
        :param header: specify header lines; default is None
        :param input_file: path of the csv file to read
        :return: df: panda data frame instance containing input data
        """

        if not os.path.exists(input_file):
            logging.error('input file "{}" not available'.format(input_file))
            sys.exit()  # event line output routine
        else:

            df = pd.read_csv(input_file, sep=sep, header=header, comment='#', engine='python')

        return df

    def get_tour_sub_phase(self):
        """
        Get Juice Tour sub-phases from Phase_1 until Phase_5 included
        :return:
        """
        sub_phase = []

        for sp in ['JUPITER_PHASE_1', 'JUPITER_PHASE_2', 'JUPITER_PHASE_3', 'JUPITER_PHASE_4', 'JUPITER_PHASE_5']:
            sub_phase.append(self.mission_phases[sp])

        return sub_phase

    def get_ganymede_sub_phase(self):
        """
        Get Juice Ganymede sub-phases from Phase_1 until Phase_5 included
        :return:
        """
        sub_phase = []

        for sp in ['GANYMEDE_PHASE_6_1', 'GANYMEDE_PHASE_6_2',
                   'GANYMEDE_PHASE_6_3', 'GANYMEDE_PHASE_6_4', 'GANYMEDE_PHASE_6_5']:

            sub_phase.append(self.mission_phases[sp])

        return sub_phase

    def get_tour_period(self):
        """
        Get Juice Tour from Phase_1 until Phase_5 included
        :return: start, end of tour
        """

        start = self.mission_phases['JUPITER_PHASE_ALL'].start
        end = self.mission_phases['JUPITER_PHASE_ALL'].end

        return start, end

    def get_ganymede_periods(self):
        """
        Get Juice Ganymede phases
        :return: start, end of tour
        """

        start = self.mission_phases['GANYMEDE_PHASE_ALL'].start
        end = self.mission_phases['GANYMEDE_PHASE_ALL'].end

        return start, end

    def get_all_periods(self):
        """
        Get Juice Ganymede phases
        :return: start, end of tour
        """

        start = self.mission_phases['MISSION_PHASE_ALL'].start
        end = self.mission_phases['MISSION_PHASE_ALL'].end

        return start, end


class MissionPhase(object):
    """
    Mission Phase
    """

    def __init__(self, id, descr, start, end):

        self.id = id
        self.description = descr
        self.start = start
        self.end = end
        self.call_roll = []

    def to_string(self):

        return '{} ; [{} - {}]; {}; '.format(self.id, self.start, self.end, self.description)
