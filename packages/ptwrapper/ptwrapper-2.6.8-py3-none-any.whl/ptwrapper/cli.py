# *****************************************************************************#
# This file is subject to the terms and conditions defined in the             #
# file 'LICENSE.txt', which is part of this source code package.              #
#                                                                             #
# No part of the package, including this file, may be copied, modified,       #
# propagated, or distributed except according to the terms contained in       #
# the file 'LICENSE.txt'.                                                     #
#                                                                             #
# (C) Copyright European Space Agency, 2025                                   #
# *****************************************************************************#
import os
import json
import sys
import shutil as sh
from argparse import ArgumentParser

from osve import osve

from .main import simulation
from .utils import dict_to_html_table, merge_logs, reorder_dict


def cli(test=False):
    """
    CLI to resolve a PTR file and generate a SPICE CK kernel.

    Parameters
    ----------
    test : bool, optional
        If True, return the argument parser for testing (default is False).
    """
    parser = setup_parser()
    args = parser.parse_args()

    validate_arguments(args)

    with open(args.ptr, 'r') as p:
        ptr_content = p.read()

    _, temp_parent_path, ptr_log = process_simulation(
        args, ptr_content
    )

    if ptr_log == -1:
        print(f'[ERROR]   {"<PTWR>":<27} PTWrapper session ended with ERRORS. Check your input files')
        temp_parent_path.cleanup()
        if test:
            return parser
        sys.exit(-1)

    handle_output(args, ptr_log, temp_parent_path)

    print(f'[INFO]    {"<PTWR>":<27} PTWrapper session ended successfully')

    if test:
        return parser


def setup_parser():
    parser = ArgumentParser(
        description='Pointing Tool Wrapper (PTWrapper) simulates a PTR and generates the '
                    'corresponding resolved PTR, SPICE CK kernels, '
                    'and other attitude related files. PTWrapper uses OSVE to simulate the PTR.'
    )

    parser.add_argument("-m", "--meta-kernel", help="[MANDATORY] Path to the SPICE Meta-kernel (MK) file")
    parser.add_argument("-p", "--ptr", help="[MANDATORY] Path to the Pointing Timeline Request (PTR) file.")
    parser.add_argument("-w", "--working-dir", default=os.getcwd(),
                        help="Path to the working directory. Default is the current directory.")
    parser.add_argument("-o", "--output-dir", help="Path to the output directory. Default is the current directory.")
    parser.add_argument("-t", "--time-step", default=5, type=int,
                        help="Simulation time step in seconds. Default is 5s.")
    parser.add_argument("-pw", "--power", action="store_true",
                        help="Calculate the available power and compare it with the one generated from the SPICE meta-kernel. Default is that the Available Power is not calculated.")
    parser.add_argument("-sa", "--sa-ck", action="store_true", help="Generate the Solar Arrays SPICE CK.")
    parser.add_argument("-mga", "--mga-ck", action="store_true", help="Generate the Medium Gain Antenna SPICE CK.")
    parser.add_argument("-q", "--quaternions", action="store_true", help="Calculate the quaternions.")
    parser.add_argument("-ro", "--remove-obs-comp", action="store_true", help="Remove the observation compatibility checks from the simulation.")
    parser.add_argument("-rc", "--remove-checks", action="store_true", help="Remove all the constraint and observation compatibility checks from the simulation (enhances performance).")
    parser.add_argument("-f", "--fixed-definitions", action="store_true",
                        help="Print the AGM Fixed Definitions in use for PTR design.")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="Keep all setup files of the OSVE simulation.")
    parser.add_argument("-v", "--version", action="store_true",
                        help="Print OSVE, AGM, and EPS libraries version.")

    return parser


def validate_arguments(args):
    if args.version:
        display_versions()
        sys.exit(1)

    if args.fixed_definitions:
        display_fixed_definitions()
        sys.exit(1)

    if not args.meta_kernel or not os.path.exists(args.meta_kernel):
        raise ValueError(f'[ERROR]    {"<PTWR>":<27} Meta-kernel not provided or does not exist')

    if not args.ptr:
        raise ValueError(f'[ERROR]    {"<PTWR>":<27} PTR/PTX file not provided')

    _, ext = os.path.splitext(args.ptr)
    if ext.lower() not in ['.xml', '.ptx', '.ptr']:
        raise ValueError(f'[ERROR]    {"<PTWR>":<27} Invalid PTR file extension')


def display_versions():
    the_osve = osve.osve()
    print("\nOSVE LIB VERSION:       ", the_osve.get_app_version())
    print("OSVE AGM VERSION:       ", the_osve.get_agm_version())
    print("OSVE EPS VERSION:       ", the_osve.get_eps_version(), "\n")


def display_fixed_definitions():
    fixed_definitions_path = os.path.join(
        os.path.dirname(__file__), "config/age", "cfg_agm_jui_fixed_definitions.xml"
    )
    try:
        with open(fixed_definitions_path, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print(f'[ERROR]    {"<PTWR>":<27} Fixed definitions file not found')
    except Exception as e:
        print(f'[ERROR]    {"<PTWR>":<27} An error occurred: {e}')


def process_simulation(args, ptr_content):
    return simulation(
        args.meta_kernel, ptr_content,
        time_step=args.time_step,
        power=args.power,
        sa_ck=args.sa_ck,
        mga_ck=args.mga_ck,
        quaternions=args.quaternions,
        remove_obs_comp=args.remove_obs_comp,
        remove_checks=args.remove_checks
    )


def handle_output(args, ptr_log, temp_parent_path):
    if args.output_dir:
        output_dir = os.path.abspath(args.output_dir)
        os.makedirs(output_dir, exist_ok=True)
    else:
        output_dir = os.getcwd()

    ptr_file_name = os.path.splitext(os.path.basename(args.ptr))[0]

    if ptr_log:
        osve_log_file = os.path.join(temp_parent_path.name, 'outputs/log.json')
        ptr_log = merge_logs(ptr_log, osve_log_file)
        create_logs(output_dir, ptr_file_name, ptr_log)

    rename_output_files(temp_parent_path, output_dir, ptr_file_name)

    if args.debug:
        moved_dir = sh.move(temp_parent_path.name, output_dir)
        print(f'[DEBUG]   {"<PTWR>":<27} OSVE setup files moved to {moved_dir}')
    else:
        temp_parent_path.cleanup()


def create_logs(output_dir, file_name, ptr_log):
    html_path = os.path.join(output_dir, f'{file_name}_ptr_log.html')
    json_path = os.path.join(output_dir, f'{file_name}_ptr_log.json')

    ptr_log = reorder_dict(ptr_log, 'SLEW ESTIMATOR')

    with open(html_path, 'w') as html_file:
        html_file.write(dict_to_html_table(ptr_log))

    with open(json_path, 'w') as json_file:
        json.dump(ptr_log, json_file)

    print(f'[INFO]    {"<PTWR>":<27} PTWrapper session log created')


def rename_output_files(temp_parent_path, output_dir, file_name):
    file_mapping = {
        'quaternions.csv': f'{file_name}_quaternions.csv',
        'juice_sa_ptr.bc': f'juice_sa_{file_name}.bc',
        'juice_mga_ptr.bc': f'juice_mga_{file_name}.bc',
        'power.csv': f'{file_name}_power.csv',
        'ptr_resolved.ptx': f'{file_name}_resolved.ptx',
        'juice_sc_ptr.bc': f'juice_sc_{file_name.lower()}_v01.bc',
        'log.json': f'{file_name}_osve_log.json'
    }

    for src, dest in file_mapping.items():
        src_path = os.path.join(temp_parent_path.name, 'outputs', src)
        if os.path.exists(src_path):
            dest_path = os.path.join(output_dir, dest)
            sh.move(src_path, dest_path)
