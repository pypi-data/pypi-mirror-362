# -*- coding: utf-8 -*-
# pylint: disable-msg=missing-class-docstring,too-few-public-methods


import jinja2

from .dummy import Templater


class JinjaTemplater(Templater):
    name = "jinja2"

    def render(self, content):
        env = jinja2.Environment()
        template = env.from_string(content)
        content = template.render()

        return content
