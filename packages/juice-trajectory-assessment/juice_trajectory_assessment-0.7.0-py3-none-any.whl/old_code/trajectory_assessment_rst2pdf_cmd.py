"""
Created on Feburary, 2021

@author: Claudio Munoz Crego (ESAC)

This Module allows to update the report.rst and re-generate the corresponding pdf.
"""


import argparse
import logging
import os
import signal
import sys

from esac_juice_pyutils.commons.my_log import setup_logger

from juice_trajectory_assessment import version
from old_code.trajectory_assessment_rst2pdf import get_template_rst2pdf, rst2pdf


def funcSignalHandler(signal, frame):
    logging.error("Aborting ...")
    logging.info("Cleanup not yet implemented")
    sys.exit(0)


def parseOptions():
    """
    This function allow to specify the input parameters
    - rst_file: rst file
    - style_template: rst to pdf template style file
    - pdf_file: path of the configuration file
    - loglevel: debug, info
    - version: package version number
    :returns args; argument o parameter list passed by command line
    :rtype list
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--rst_file",
                        help="Path rst input file",
                        required=True)

    parser.add_argument("-s", "--style_template",
                        help="Path rst to pdf style file",
                        required=False)

    parser.add_argument("-o", "--pdf_file",
                        help="Path pdf output file",
                        required=False)

    parser.add_argument("-l", "--loglevel",
                        help=" Must be debug, info ",
                        required=False)

    parser.add_argument("-v", "--version",
                        help="version number",
                        action="version",
                        version='%(prog)s {}'.format(version))

    args = parser.parse_args()
    return args


def main():
    """
        Entry point for processing

        :return:
        """

    signal.signal(signal.SIGINT, funcSignalHandler)

    args = parseOptions()

    if args.loglevel:
        if args.loglevel in ['info', 'debug']:
            setup_logger(args.loglevel)
        else:
            setup_logger()
            logging.warning(
                'log level value "{0}" not valid (use debug);  So default INFO level applied'.format(args.loglevel))
    else:
        setup_logger()

    if args.rst_file:
        if not os.path.exists(args.rst_file):
            logging.error('rst input file "{}" does not exist'.format(args.rst_file))
            sys.exit(0)
        else:
            rst_file = os.path.abspath(args.rst_file)
    else:
        logging.error('Please define rst Configuration File')
        sys.exit(0)

    if args.style_template:
        if not os.path.exists(args.style_template):
            logging.info('rst input file "{}" does not exist'.format(args.style_template))
            sys.exit(0)
        else:
            style_template = os.path.abspath(args.rst_file)
    else:
        style_template = get_template_rst2pdf()

    if args.pdf_file:

        pdf_file = args.pdf_file

    else:
        pdf_file = str(rst_file).replace('.rst', '.pdf')

    here = os.path.abspath(os.path.dirname(rst_file))

    working_dir = os.path.dirname(rst_file)

    os.chdir(working_dir)
    logging.info('Working directory: {}'.format(working_dir))

    rst2pdf(rst_file, pdf_file, style_file=style_template)

    os.chdir(here)
    logging.debug('goto root original directory: {}'.format(here))


def debug():
    """
    debug: Print exception and stack trace
    """

    e = sys.exc_info()
    print("type: %s" % e[0])
    print("Msg: %s" % e[1])
    import traceback
    traceback.print_exc(e[2])
    traceback.print_tb(e[2])


if __name__ == "__main__":

    try:
        main()
    except SystemExit as e:
        print("Exit")
    except:
        print("<h5>Internal Error. Please contact JUICE SOC </h5>")
        debug()

    sys.exit(0)

