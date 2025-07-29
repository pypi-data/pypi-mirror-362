# SPDX-FileCopyrightText: 2025 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

import pytest

from pully.cli import parser


@pytest.mark.parametrize(
    "argv,funcname,expected",
    (
        (["add", "-p", "70752539"], "add_command", dict(project_id=70752539)),
        (
            ["add", "-P", "saferatday0/badgie"],
            "add_command",
            dict(project_path="saferatday0/badgie"),
        ),
        (["add", "-g", "78192659"], "add_command", dict(group_id=78192659)),
        (["add", "-G", "saferatday0"], "add_command", dict(group_path="saferatday0")),
        ([], "sync_command", dict()),
    ),
)
def test_parse_args(argv, funcname, expected):
    args = parser.parse_args(argv)
    assert args.func.__name__ == funcname
    for key, value in expected.items():
        assert getattr(args, key) == value
