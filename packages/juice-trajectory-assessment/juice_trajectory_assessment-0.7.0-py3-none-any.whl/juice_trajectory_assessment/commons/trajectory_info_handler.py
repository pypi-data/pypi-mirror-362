"""
Created on July, 2020

@author: Claudio Munoz Crego (ESAC)

This Module allows to handle trajectory info

"""

import os
import sys
import logging
import datetime
import pandas as pd

import numpy as np


class TrajectoryInfo(object):
    """
    This Class allows read and parse trajectory info file
    """

    def __init__(self, file_input, output_dir="./"):

        self.output_dir = output_dir

        self.traj_info = self.read(file_input)

    def read(self, input_file, nb_digits=2):
        """
        Read Trajectory info

        :param input_file: input file
        :param nb_digits: number of digit for float rounding
        :return: traj_info: dictionary including key, value
        """

        def my_round_float(v):

            if v.is_integer():
                return str(int(v))
            else:
                return str(round(float(v), ndigits=nb_digits))

        logging.debug('Reading file: {}'.format(input_file))

        if not os.path.exists(input_file):
            logging.error('File does not exist: {}'.format(input_file))
            sys.exit()

        else:
            # df = pd.read_csv(input_file, sep=',', header=[0], comment='#', engine='python')
            # # traj_info = df.to_dict('records')[0]
            #
            # df = df.fillna("")
            #
            # traj_info = {}
            # for k in df.keys():
            #     print(df[k])
            #     traj_info[k] = [float(df[k][1]), df[k][0], ]

            f = open(input_file, 'r')

            lines = f.readlines()
            param = lines[1].replace('"', '').rstrip('\n').split(',')
            values = lines[2].replace('"', '').rstrip('\n').split(',')
            units = lines[0].replace('"', '').rstrip('\n').split(',')

            traj_info = {}

            # print(len(param))
            # print(len(values))
            # print(len(units))
            for i in range(len(param)):

                # if isinstance(values[i], float) or isinstance(values[i], int)

                # print('{}: {}: {}'.format(i, param[i], values[i]))

                if values[i] == "" or values is None or values[i].strip() == "":
                    val = ""

                elif (param[i].endswith('_FB') or param[i].endswith('_ECLIPSE')) and ':' in values[i]:
                    val = values[i]
                    if not val.startswith('\\n'):
                        val = '[' + val.replace('\\n', '\\n\\n[')
                    else:
                        val = val[2:].replace('\\n', '\\n\\n[')
                    val = val.replace(':', ']:')
                    # val = val.split('\\n')
                    # n = 3
                    # val = [', '.join(val[i:i + n]) for i in range(0, len(val), n)]
                    # val = ',\\n'.join(val)

                elif param[i].startswith('FB') or param[i].startswith('PE'):
                    val = values[i]

                elif values[i][0].isdigit():
                    if ' ' in values[i]:
                        val = values[i].strip(' ').split()
                        val = [str(round(float(v), ndigits=nb_digits)) for v in val]
                        val = '\\n'.join(val)
                    elif '/n' in values[i]:
                        val = values[i].split('/n')
                        val = [str(round(float(v), ndigits=nb_digits)) for v in val]
                        val = '\\n'.join(val)
                    elif '\\n' in values[i]:
                        val = values[i].split('\\n')
                        if val[0].isdigit():
                            val = [str(round(float(v), ndigits=nb_digits)) for v in val]
                        n = 5
                        val = [', '.join(val[i:i + n]) for i in range(0, len(val), n)]
                        val = ',\\n'.join(val)
                    else:
                        val = float(values[i])
                        val = my_round_float(val)  # str(round(val, ndigits=nb_digits))

                elif param[i] == 'KERNEL_LIST':
                    val = values[i]
                    val = val.replace('$KERNELS/', '')
                    val = val.replace('\'', '')
                    val = val.replace('.bsp)', '.bsp')
                    val = sorted(val.split('\\n'))
                    val = '\\n\\n'.join(val)

                elif 'DATES_SOLAR_CONJUNCTIONS' in param[i]:
                    val = values[i]
                    n_count = val.count('UNTIL')
                    val = val.replace(' UNTIL ', ', ')
                    if val.endswith(' / '):
                        val = val[:-3]
                    val = val.replace('conjunctions: ',
                                      'conjunctions:\\n\\n[')
                    val = val.replace(' / ', ']\\n\\n[')
                    val = '{} {}]'.format(n_count, val)

                else:
                    val = values[i]

                # print(val)
                traj_info[param[i]] = [val, units[i]]

            f.close()

        return traj_info

    def pd2metric(self):
        """
        translate dico to key values list with header
        :return: metrics, a list of list containing metrics lists with headers in first row
        """

        metrics = [['Parameters', 'values', 'Units']]

        for k, v in self.traj_info.items():
            metrics.append([k, v[0], v[1]])

        return metrics

    def pd2simpledico(self):
        """
        translate dico to key values list with header
        :return: metrics, a list of list containing metrics lists with headers in first row
        """

        metrics = [['Parameters', 'values']]

        for k, v in self.traj_info.items():

            if k.startswith("FB_") or k.startswith("PERI_") or k.startswith("SUBSC_VEL_"):
                continue

            unit = ''
            if v[1]:
                unit = " [{}]".format(v[1])

            metrics.append([k + unit, v[0]])

        return metrics

    def pd2fbdico(self):
        """
        translate dico to FB key values list with header
        :return: metrics, a list of list containing metrics lists with headers in first row
        """
        full_list = ["FB_LIST_NAMES", "FB_TIME_UTC", "FB_ALTITUDE", "FB_SSC_LON", "FB_SSC_LAT", "FB_SSC_PHASE",
                   "FB_SSC_LOCTIME", "FB_JUP_MOON_SC_ANG", "FB_MOON_TRUE_ANOM", "FB_NIM_FOV_OBSTR",
                   "FB_MAX_SC_SUN2YZ_PLANE_DURING_PB",
                   "FB_MALARGUE_AT_CA", "FB_CEBREROS_AT_CA", "FB_DELTA_TIME_PERIJOVE", "FB_FLIGHT_DIRECTION",
                   "FB_IN_JUP_ECLIPSE", "FB_EARTH_OCC_DURING_FB", "FB_MOON_ANG_SIZE"]

        in_list = ["FB_LIST_NAMES", "FB_TIME_UTC", "FB_ALTITUDE", "FB_SSC_LON", "FB_SSC_LAT", "FB_SSC_PHASE",
                   "FB_JUP_MOON_SC_ANG", "FB_MOON_TRUE_ANOM"]

        in_list_2 = ["FB_LIST_NAMES", "FB_SSC_LOCTIME", "FB_MAX_SC_SUN2YZ_PLANE_DURING_PB",
                   "FB_MALARGUE_AT_CA", "FB_CEBREROS_AT_CA", "FB_DELTA_TIME_PERIJOVE", "FB_FLIGHT_DIRECTION",
                   "FB_IN_JUP_ECLIPSE", "FB_EARTH_OCC_DURING_FB", "FB_MOON_ANG_SIZE"]

        metrics = []

        for k, v in self.traj_info.items():

            if k.startswith("FB_"):

                if k not in in_list:
                    continue

                if k == 'FB_LIST_NAMES':

                    param = 'ID'

                else:

                    param = ' '.join(k.split('_')[1:])

                    if v[1]:  # V[1] can contains unit

                        param = "{} [{}]".format(param, v[1])

                values = v[0].split()

                metrics.append([param] + values)

        metrics = np.array(metrics).T.tolist()

        return metrics

    def pd2perijovedico(self):
        """
        translate dico to Perijove key values list with header
        :return: metrics, a list of list containing metrics lists with headers in first row
        """

        metrics = []

        for k, v in self.traj_info.items():

            if k.startswith("PERI_"):

                if k == 'PERI_LIST_NAME':

                    param = 'ID'

                else:

                    param = ' '.join(k.split('_')[1:])

                    if v[1]:  # V[1] can contains unit

                        param = "{} [{}]".format(param, v[1])

                values = v[0].split()

                metrics.append([param] + values)

        metrics = np.array(metrics).T.tolist()

        return metrics

    def pd2cruisedico(self):
        """
        translate dico to Flybys Cruise key values list with header
        :return: metrics, a list of list containing metrics lists with headers in first row
        """

        metrics = []

        for k, v in self.traj_info.items():

            if k.startswith("FB_CRUISE_"):

                if k == 'FB_CRUISE_LIST_NAME':

                    param = 'ID'

                else:

                    param = ' '.join(k.split('_')[2:])

                    if v[1]:  # V[1] can contains unit

                        param = "{} [{}]".format(param, v[1])

                values = v[0].split()

                metrics.append([param] + values)

        metrics = np.array(metrics).T.tolist()

        from operator import itemgetter

        metrics[1:] = sorted(metrics[1:], key=itemgetter(1))

        return metrics






