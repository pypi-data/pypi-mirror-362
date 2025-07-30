# -*- coding: utf-8 -*-
# pylint: disable-msg=missing-function-docstring


import bignole.core.lexer
import bignole.core.parser


def process(content):
    content = content.split("\n")
    content = bignole.core.lexer.lex(content)
    content = bignole.core.parser.parse(content)
    content = generate(content)
    content = "\n".join(content)

    return content


def generate(tree):
    for host in flat(tree):
        yield f"Host {host.fullname}"

        for option, values in sorted(host.options.items()):
            for value in sorted(values):
                yield f"    {option} {value}"

        yield ""


def flat(tree):
    for host in sorted(tree.childs, key=lambda h: (h.name == "*", h.name)):
        yield from flat_host_data(host)


def flat_host_data(tree):
    for host in tree.hosts:
        yield from flat_host_data(host)

    if tree.trackable:
        if not (tree.fullname == "*" and not tree.options):
            yield tree
