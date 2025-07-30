# SPDX-FileCopyrightText: 2025 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

import argparse

from .._version import __version__
from .add_command import add_command
from .init_command import init_command
from .sync_command import sync_command


def get_parser():
    parser = argparse.ArgumentParser()
    # parser.add_argument("-C", "--directory", type=str)
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.set_defaults(func=sync_command)

    subparsers = parser.add_subparsers(required=False)

    add_parser = subparsers.add_parser("add")
    add_parser.set_defaults(func=add_command)

    id_group = add_parser.add_mutually_exclusive_group(required=True)
    id_group.add_argument("-g", "--group-id", type=int)
    id_group.add_argument("-G", "--group-path", type=str)
    id_group.add_argument("-p", "--project-id", type=int)
    id_group.add_argument("-P", "--project-path", type=str)

    init_parser = subparsers.add_parser("init")
    init_parser.set_defaults(func=init_command)

    sync_parser = subparsers.add_parser("sync")
    sync_parser.set_defaults(func=sync_command)

    return parser


def parse_args(args=None):
    parser = get_parser()
    return parser.parse_args(args=args)
