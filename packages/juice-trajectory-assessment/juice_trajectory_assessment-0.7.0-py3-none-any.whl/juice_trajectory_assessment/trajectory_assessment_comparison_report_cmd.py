"""
Created on January 2021

@author: Claudio Munoz Crego (ESAC)

This Module generates Trajectory Assessment Comparison Report which using:
 - EPS output
 - Geopipeline parameter via csv files
 - coverage via Coverage tool

which allows to compare a collection of/parameter corresponding to 2 different crema

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
from juice_trajectory_assessment.comparison_report.comparison_report import ComparisonReport


def func_signal_handler(signal, frame):
    logging.error("Aborting ...")
    logging.info("Cleanup not yet implemented")
    sys.exit(0)


def parse_options():
    """
    This function allow to specify the input parameters
    - startDate: start date of event to produce YYYY-mm-DD
    - endDate: end date of event to produce YYYY-mm-DD
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
        logging.error('Please define Configuration File')
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

    cfg_main = cfg['main']
    output_dir = cfg_main['output_dir']

    crema_list = cfg_main['crema_list']
    crema_ref = crema_list[0]
    crema_2compare = crema_list[1]

    for k, v in cfg_main['env_var'].items():
        for k_i, v_i in cfg_main['env_var'].items():
            if k_i in v:
                cfg_main['env_var'][k] = cfg_main['env_var'][k].replace(k_i, v_i)

    env_var = EnvVar(cfg_main['env_var'])

    report_title = cfg_main['title']
    report_orientation_landscape = cfg_main['report_orientation_landscape']

    report_name = None
    if 'report_name' in cfg_main.keys():
        report_name = cfg_main['report_name']

    juice_conf = None
    path_to_osve_lib_dir = None
    kernel = None
    generate_pdf = False

    if 'juice_conf' in cfg_main.keys():
        juice_conf = cfg_main['juice_conf']

    if 'path_to_osve_lib_dir' in cfg_main.keys():
        path_to_osve_lib_dir = cfg_main['path_to_osve_lib_dir']

    if 'kernel' in cfg_main.keys():
        kernel = cfg_main['kernel']

    run_simu = True
    if 'run_sim' in cfg_main.keys():
        run_simu = cfg_main['run_sim']

    include_dv_section = True
    if 'include_dv_section' in cfg_main.keys():
        include_dv_section = cfg_main['include_dv_section']

    include_cruise = True
    if 'include_cruise' in cfg_main.keys():
        include_cruise = cfg_main['include_cruise']

    docx_template = None
    if 'docx_template' in cfg_main.keys():
        docx_template = cfg_main['docx_template']

    start = end = None  # not needed at least for now; TODO Remove them
    p = ComparisonReport(start, end, env_var, output_dir=output_dir)

    p.set_crema_ref(crema_ref, cfg_main['crema_details'][crema_ref],
                    juice_conf=juice_conf, path_to_osve_lib_dir=path_to_osve_lib_dir,
                    kernel=kernel, run_simu=run_simu,
                    include_dv_section=include_dv_section, include_cruise=include_cruise)

    p.set_crema_2compare(crema_2compare, cfg_main['crema_details'][crema_2compare],
                         juice_conf=juice_conf, path_to_osve_lib_dir=path_to_osve_lib_dir,
                         kernel=kernel, run_simu=run_simu,
                         include_dv_section=include_dv_section, include_cruise=include_cruise)

    p.create_report(working_dir, output_dir, report_title=report_title,
                    report_orientation_landscape=report_orientation_landscape,
                    new_report_name=report_name,
                    docx_template=docx_template,
                    generate_pdf=generate_pdf)


def generate_configuration_file_template():
    """
    Generate a local copy of the template configuration file
    """

    here = os.path.abspath(os.path.dirname(__file__))
    template_path = os.path.join(here, 'templates', 'traj_assessment_comparison_report.json')
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
        print(e)
        print("<h5>Internal Error. Please contact JUICE SOC </h5>")
        raise

    sys.exit(0)
