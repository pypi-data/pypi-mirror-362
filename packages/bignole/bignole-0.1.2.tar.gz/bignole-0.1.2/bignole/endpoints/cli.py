# -*- coding: utf-8 -*-


import argparse

import bignole
import bignole.templater


def create_parser():
    """Create a argparse.ArgumentParser with all the needed arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--debug",
        help="Run %(prog)s in debug mode.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Run %(prog)s in verbose mode.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-s",
        "--source-path",
        help=f"Path of bignole. Default is {bignole.DEFAULT_RC}",
        default=bignole.DEFAULT_RC,
    )
    parser.add_argument(
        "-o",
        "--destination-path",
        help=(
            "Path of ssh config. If nothing is set, then prints to stdout. "
            "Otherwise, stores into file."
        ),
        default=None,
    )
    parser.add_argument(
        "-b",
        "--boring-syntax",
        help="Use old boring syntax, described in 'man 5 ssh_config'.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-a",
        "--add-header",
        help=(
            "Prints header at the top of the file. "
            "If nothing is set, then the rule is: if DESTINATION_PATH "
            "is file, then this option is true by default. If "
            "DESTINATION_PATH is stdout, then this option is set to false."
        ),
        action="store_true",
        default=None,
    )
    parser.add_argument(
        "-u",
        "--use-templater",
        help=(
            "Use following templater for config file. If nothing is set, "
            "then default template resolve chain will be "
            "used (Mako -> Jinja -> Nothing). Dummy templater means that "
            "no templater is actually used."
        ),
        choices=bignole.templater.all_templaters().keys(),
        default=None,
    )

    return parser
