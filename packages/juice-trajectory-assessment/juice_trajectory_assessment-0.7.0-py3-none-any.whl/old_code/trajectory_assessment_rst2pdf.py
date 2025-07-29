"""
Created on Feburary, 2021

@author: Claudio Munoz Crego (ESAC)

This Module allows to update the report.rst and re-generate the corresponding pdf.
"""

import os
import sys
import logging
import subprocess


def rst2pdf(rst_report, pdf_report, style_file=None):
    """
    Convert rst to pdf file using rst2pdf tool and optionally a style file

    :param rst_report: path of input rst file
    :param pdf_report: path of output pdf file
    :param style_file: rst2pdf style file
    :return:
    """

    f_in = rst_report
    f_out = pdf_report

    command = 'rst2pdf {} {} '.format(f_in, f_out)

    if style_file:

        command = 'rst2pdf {} -s {} {} '.format(f_in, style_file, f_out)

    logging.info('running os command "{}'.format(command))

    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        while True:
            line = p.stdout.readline()
            if not line: break
            print('{}'.format(line))
        p.wait()

        if p.returncode != 0:
            p.terminate()

        logging.info('file {} generated '.format(f_out))

    except Exception:
        logging.error('command failed:  {} '.format(command))
        logging.warning('file {} cannot be generated '.format(f_out))


def get_template_rst2pdf():
    """
    Get the rst2pdf.style template hosted in source code within templates sub-directory

    :return: rst2pdf.style  path
    :rtype: python path
    """

    here = os.path.abspath(os.path.dirname(__file__))
    template_file = os.path.join(here, '../juice_trajectory_assessment/report/templates')
    template_file = os.path.join(template_file, 'default_rst2pdf.style')

    if not os.path.exists(template_file):
        logging.error('reference template file "%s" missing' % template_file)
        sys.exit()

    logging.info('{} loaded'.format(template_file))
