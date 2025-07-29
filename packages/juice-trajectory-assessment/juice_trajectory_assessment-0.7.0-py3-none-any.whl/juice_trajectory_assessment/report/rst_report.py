"""
Created on February, 2018

@author: Claudio Munoz Crego (ESAC)

This Module allows to generate an rst report
"""

import logging
import os
import sys
import numpy as np

from esac_juice_pyutils.commons.rst_handler import RstHandler


class RstReport(RstHandler):
    """
    This class allows to generate an rst report
    """

    def __init__(self, input_path, output_path='', out=sys.stdout):
        """
        :param output_path:
        :param out:
        :param input_path: path of directory containing plots
        """

        if not os.path.exists(input_path):
            logging.error('input path "{}" does not exist'.format(input_path))
        else:
            self.input_path = os.path.abspath(os.path.expandvars(input_path))

        if output_path == '':
            output_path = self.input_path
            if not os.path.exists(output_path):
                logging.error('output path "{}" does not exist'.format(output_path))

        self.output_dir = output_path

        super(RstReport, self).__init__(output_path, out)

    def print_summary_intro(self, title='Title', objective_summary='', metrics=[]):
        """
        Produces summary intro

        :objectif_summary: summary of the objective of study
        """

        if isinstance(title, list):

            for line in  title:

                self.write_head_chapter(line)

            self.out.write('\n')

        else:

            self.write_head_chapter(title)

        self.out.write('.. contents:: Table of Contents\n')
        self.insert_page_break()

        if objective_summary != '':
            self.out.write('\n' + objective_summary + '\n')

        if len(metrics) > 0:
            self.print_rst_table(metrics)

    def print_summary_end(self):
        """
        Produces summary end
        """

        self.out.close()

        logging.info('rst file {} generated'.format(self.rst_file_name))

    def print_summary_subsection(self, title, objective_summary='', metrics=[], figure=[]):
        """
        Produces summary intro

        :objectif_summary: summary of the objective of study
        """

        self.write_head_subsection(title)
        if objective_summary != '':
            self.out.write('\n' + objective_summary + '\n')

        if len(metrics) > 0:
            self.print_rst_table(metrics)
            self.out.write('\n')

        else:

            self.out.write('No data for this period!')
            self.out.write('\n\n')

        if len(figure) > 0:
            for fig in figure:
                fig = os.path.expandvars(fig)
                if not os.path.exists(fig):
                    logging.error('input path "{}" does not exist'.format(fig))
                else:
                    self.rst_insert_figure(fig, title=title, text=objective_summary)

    def print_table(self, title, metrics=[]):
        """
        include table in report
        :return:
        """

        if len(metrics) > 0:

            self.print_rst_csv_table(metrics, title)
            self.out.write('\n')

    def print_summary_sub_subsection(self, title, objective_summary='', metrics=[], figure=[]):
        """
        Produces summary intro

        :objectif_summary: summary of the objective of study
        """

        self.write_head_subsubsection(title)
        if objective_summary != '':
            self.out.write('\n' + objective_summary + '\n')

        if len(metrics) > 0:

            self.print_rst_csv_table(metrics, title)
            self.out.write('\n')

        if len(figure) > 0:
            for fig in figure:
                fig = os.path.expandvars(fig)
                self.rst_insert_figure(fig, title=title, text=objective_summary)

    def create_plot_pie(self, plots_path, title, percent, min_values=0):
        """
        Create pie plot

        :param min_values: the min value to plot, i.e. 0.01 %; mainly remove too small values
        :param plots_path:
        :param title:
        :param percent:
        :return:
        """

        import matplotlib.pyplot as plt

        percent_keys = list(percent.keys())
        for k in reversed(percent_keys):
            if percent[k] < min_values:
                del percent[k]

        labels = sorted(percent.keys())
        sizes = [percent[k] for k in labels]
        labels = ['{} [{}%]'.format(k, percent[k]) for k in labels]
        explode = [i % 2 * 0.1 for i, x in enumerate(percent.keys())]

        pies = plt.pie(sizes, startangle=90, autopct='%1.0f%%', pctdistance=0.9, radius=1.2,
                       explode=explode)

        plt.legend(pies[0], labels, bbox_to_anchor=(1, 0.5), loc="center right", fontsize=8,
                   bbox_transform=plt.gcf().transFigure)
        plt.subplots_adjust(left=0.0, bottom=0.1, right=0.50)

        plt.axis('equal')
        plot_file_path = os.path.join(plots_path, title.replace(' ', '_') + '.png')
        plt.savefig(plot_file_path)
        plt.close()

        return plot_file_path

    def print_rst_table_2(self, metrics, title=True, return_line_sep='\\n'):
        """
        Generate (print) a table in rst format

        :param title: flag which specify if the table have a title line or not.
        :param metrics: list of table lines, if title=True, the title must be in metrics[0]
        :param return_line_sep: separato
        """

        self.out.write('\n')

        d = [0] * len(metrics[0])

        extended_metrics = []
        for line in metrics:
            nb_of_next_line = 0
            for cell in line:
                if not isinstance(cell, str):  # avoid non string casting them str
                    cell = str(cell)
                if cell.count(return_line_sep) > nb_of_next_line:
                    nb_of_next_line = cell.count(return_line_sep)

            columns = []
            n_col = len(line)

            if n_col > len(d):
                logging.error('more column values than header in metrics; {} > {}'.format(n_col, len(d)))
                # if theere are less filed by 0

            for i in range(n_col):
                cell = line[i]
                if not isinstance(cell, str):  # avoid non string casting them str
                    cell = str(cell)

                column = [''] * (nb_of_next_line + 1)
                sub_lines = cell.split(return_line_sep)
                sub_lines = [str(ele) for ele in sub_lines]
                if len(max(sub_lines, key=len)) > d[i]:  # adjust column size
                    d[i] = len(max(sub_lines, key=len))
                column[:len(sub_lines)] = sub_lines
                columns.append(column)

            rows = [list(i) for i in zip(*columns)]
            extended_metrics.append(rows)

        metrics = extended_metrics

        table_title_format = '|'
        table_line_format = '|'

        for i in range(len(metrics[0][0])):  # we use the first line of the title (Most of time there is only one)

            table_title_format += ' {' + str(i) + ':' + str(d[i]) + 's} |'
            table_line_format += ' {' + str(i) + ':' + str(d[i]) + 's} |'
        table_title_format += '\n'
        table_line_format += '\n'

        table_line = ''
        table_line_title = ''
        for i in range(len(d)):
            table_line += '+{}'.format('-' * (d[i] + 2))
            table_line_title += '+{}'.format('=' * (d[i] + 2))

        table_line += '+\n'
        table_line_title += '+\n'

        if title:
            self.out.write(table_line)

            for ele in metrics[0]:
                # print(table_title_format.format(*ele))
                self.out.write(table_title_format.format(*ele))
            self.out.write(table_line_title)

            metrics.pop(0)

        else:
            self.out.write(table_line)

        for ele in metrics:
            for sub_ele in ele:
                # print(table_line_format.format(*sub_ele))
                self.out.write(table_line_format.format(*sub_ele))
            self.out.write(table_line)

        self.out.write('\n')
