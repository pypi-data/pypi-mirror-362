"""
Created on July 2020

@author: Claudio Munoz Crego (ESAC)

"This Module generates Trajectory Assessment Report using:
 - EPS output
 - Geopipeline parameter via csv files
 - coverage via Rozenn Coverage tool

 in addition, some derived parameters are included in the report

"""

import argparse
import logging
import os
import shutil
import signal
import sys

from esac_juice_pyutils.commons.my_log import setup_logger
from esac_juice_pyutils.commons import json_handler as my_json
from esac_juice_pyutils.commons.env_variables import EnvVar

from juice_trajectory_assessment import version
from juice_trajectory_assessment.report.traj_assessment_report import TrajAssessmentFilter

setup_logger()


def func_signal_handler(signal, frame):
    logging.error("Aborting ...")
    logging.info("Cleanup not yet implemented")
    sys.exit(0)


def parse_options():
    """
    This function allow to specify the input parameters
    - JsonFile: path of the configuration file
    - loglevel: debug, info
    - version: package version number
    :returns args; argument o parameter list passed by command line
    :rtype list
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--JsonFile",
                        help="Path of JsonFile defining report to be generated",
                        required=False)

    parser.add_argument("-l", "--loglevel",
                        help=" Must be debug, info ",
                        required=False)

    parser.add_argument("-v", "--version",
                        help="return version number and exit",
                        action="version",
                        version='%(prog)s {}'.format(version))

    parser.add_argument("-g", "--getTemplate",
                        help="generate a configuration file template and exit",
                        action="store_true")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    return args


def main():
    """
    Entry point for processing

    :return:
    """

    signal.signal(signal.SIGINT, func_signal_handler)

    args = parse_options()

    if args.loglevel:
        if args.loglevel in ['info', 'debug']:
            setup_logger(args.loglevel)
        else:
            setup_logger()
            logging.warning(
                'log level value "{0}" not valid (use debug);  So default INFO level applied'.format(args.loglevel))
    else:
        setup_logger()

    here = os.path.abspath(os.path.dirname(__file__))

    if args.getTemplate:
        generate_configuration_file_template()

    if args.JsonFile:
        if not os.path.exists(args.JsonFile):
            logging.error('Configuration File "{}" does not exist'.format(args.JsonFile))
            sys.exit(0)
        else:
            cfg_file = os.path.abspath(args.JsonFile)

    else:
        logging.error('Please define Configuration File ')
        sys.exit(0)

    working_dir = os.path.dirname(cfg_file)
    cfg = my_json.load_to_dic(cfg_file)

    os.chdir(working_dir)

    logging.info('goto root working directory: {}'.format(working_dir))

    run(cfg_file, cfg, working_dir)

    os.chdir(here)
    logging.debug('goto root original directory: {}'.format(here))


def run(cfg_file, cfg, working_dir):
    """
    Launch reporter generation

    :param cfg: configuration para
    :param working_dir: working directory
    """

    if "config_for_command_line_tool" in list(cfg.keys()):
        name_current_module = os.path.basename(str(sys.modules[__name__]))
        if '_cmd' in name_current_module:
            name_current_module = name_current_module.split('_cmd')[0]
        if cfg['config_for_command_line_tool'] != name_current_module:
            logging.error('The config file "{}" is to run "{}" and not "{}"'.format(
                cfg_file, cfg['config_for_command_line_tool'], name_current_module
            ))
            sys.exit()

    output_dir = cfg['main']['output_dir']

    env_var, report_title, report_name, run_simu = set_parameters(cfg)

    start = end = None  # not needed at least for now; TODO Remove them
    p = TrajAssessmentFilter(start, end, env_var, output_dir=output_dir)

    p.set_crema_ref('id', cfg, run_simu=run_simu)
    p.create_report(working_dir, output_dir,
                    report_title=report_title,
                    objective='',
                    new_report_name=report_name)


def set_parameters(cfg):
    """
    Set_up parameters

    :param cfg: configuration parameters
    :return: output_dir, report_title, report_name, run_simu
             output path directory,
             report title
             report file name
             Flag to enable/disable osve simulation
    """

    cfg_main = cfg['main']

    if 'env_var' in cfg_main.keys():

        env_var = EnvVar(cfg_main['env_var'])

        for k, v in cfg['main'].items():

            if isinstance(v, str):
                cfg['main'][k] = env_var.subsitute_env_vars_in_path(v)

        if 'other_plots' in cfg_main['title']:

            for i in range(len(cfg['main']['other_plots'])):
                cfg['main']['other_plots'][i] = env_var.subsitute_env_vars_in_path(cfg['main']['other_plots'][i])

    report_title = cfg_main['title']

    report_name = None
    if 'report_name' in cfg_main.keys():
        report_name = cfg_main['report_name']

    if 'osve' in cfg.keys():

        for k, v in cfg['osve'].items():

            if isinstance(v, str):
                cfg['osve'][k] = env_var.subsitute_env_vars_in_path(v)

    run_simu = True
    if 'run_sim' in cfg_main.keys():
        run_simu = cfg_main['run_sim']

    return env_var, report_title, report_name, run_simu


def generate_configuration_file_template():
    """
    Generate a local copy of the template configuration file
    """

    here = os.path.abspath(os.path.dirname(__file__))
    template_path = os.path.join(here, 'templates', 'traj_assessment_report.json')
    template_path_local_copy = os.path.join(os.getcwd(), os.path.basename(template_path))
    shutil.copyfile(template_path, template_path_local_copy)
    logging.info('configuration template file generated: {}'.format(template_path_local_copy))
    sys.exit(0)


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
