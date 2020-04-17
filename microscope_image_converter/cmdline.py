"""
Created on Feb 19, 2018

@author: dgrewal
"""
import json
import os

import argparse
import pypeliner
from microscope_image_converter import __version__
from microscope_image_converter.config import generate_batch_config
from microscope_image_converter.config import generate_pipeline_config


class parseSentinelPattern(argparse.Action):

    def __call__(self, parser, args, values, option_string=None):
        if values.startswith("/"):
            values = values[1:]

        values = values.split("/")

        parsed = [values[0], "/".join(values[1:])]

        setattr(args, self.dest, parsed)


class parseRegionTemplate(argparse.Action):

    def __call__(self, parser, args, values, option_string=None):
        if "{region}" not in values and "{reads}" not in values:
            raise parser.error(
                "the split template should contain {region} or {reads}"
            )
        setattr(args, self.dest, values)


def separate_pypeliner_dirs_by_subcommand(args):
    if args['which'] in ['generate_config', 'clean_sentinels']:
        return args

    pipelinedir = args.get("pipelinedir", None)
    if pipelinedir:
        subcommand_name = args.get("which", None)
        if not subcommand_name:
            return args
        args["pipelinedir"] = os.path.join(pipelinedir, subcommand_name)

    pipelinedir = args.get("tempdir", None)
    if pipelinedir:
        subcommand_name = args.get("which", None)
        if not subcommand_name:
            return args
        args["tempdir"] = os.path.join(pipelinedir, subcommand_name)

    return args


def add_global_args(parser, dont_add_input_yaml=False):
    pypeliner.app.add_arguments(parser)

    if not dont_add_input_yaml:
        parser.add_argument("--input_yaml",
                            required=True,
                            help='''yaml file with fastq files, output bams and cell metadata''')

    parser.add_argument("--out_dir",
                        required=True,
                        help='''Path to output directory.''')

    config_args = parser.add_mutually_exclusive_group()

    config_args.add_argument(
        "--config_file",
        help='''Path to output directory.''')

    config_args.add_argument(
        "--config_override",
        type=json.loads,
        help='''json string to override the defaults in config''')

    parser.add_argument('--run_with_docker', help='launches pipeline in a docker container')

    return parser


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--version', action='version',
                        version='{version}'.format(version=__version__))

    subparsers = parser.add_subparsers()

    # ===========
    # convert
    # ===========
    conversion = add_global_args(subparsers.add_parser("convert"))
    conversion.set_defaults(which='conversion')

    # ======================================
    # generates pipeline and batch configs
    # ======================================
    generate_config = subparsers.add_parser("generate_config")
    generate_config.set_defaults(which='generate_config')

    generate_config.add_argument("--pipeline_config",
                                 help='''output yaml file''')

    generate_config.add_argument("--batch_config",
                                 help='''output yaml file''')

    generate_config.add_argument("--config_override",
                                 type=json.loads,
                                 help='''json string to override the defaults in config''')

    # ============================
    # remove tasks from sentinels
    # ============================
    clean_sentinels = subparsers.add_parser("clean_sentinels")
    clean_sentinels.set_defaults(which='clean_sentinels')

    clean_sentinels.add_argument("--mode",
                                 required=True,
                                 choices=['list', 'delete'],
                                 help='''list or delete''')

    clean_sentinels.add_argument("--pattern",
                                 action=parseSentinelPattern,
                                 required=True,
                                 help='''pattern to clean''')

    clean_sentinels.add_argument("--pipelinedir",
                                 required=True,
                                 help='''path to the pipeline dir''')

    args = vars(parser.parse_args())

    # add config paths to global args if needed.
    args = generate_pipeline_config.generate_pipeline_config_in_temp(args)

    args = generate_batch_config.generate_submit_config_in_temp(args)

    # separate pipelinedirs of subcommands
    args = separate_pypeliner_dirs_by_subcommand(args)

    return args
