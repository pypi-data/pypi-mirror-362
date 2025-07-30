# -*- coding: utf-8 -*-


import bignole
from bignole.endpoints import cli


def test_parser_default(cliargs_default):
    parser = cli.create_parser()
    parsed = parser.parse_args()

    assert not parsed.debug
    assert not parsed.verbose
    assert parsed.source_path == bignole.DEFAULT_RC
    assert parsed.destination_path is None
    assert not parsed.boring_syntax
    assert parsed.add_header is None
