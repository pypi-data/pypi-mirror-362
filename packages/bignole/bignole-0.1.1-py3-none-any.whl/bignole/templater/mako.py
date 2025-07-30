# -*- coding: utf-8 -*-
# pylint: disable-msg=missing-class-docstring,too-few-public-methods

import mako.template

from .dummy import Templater


class MakoTemplater(Templater):
    name = "mako"

    def render(self, content):
        template = mako.template.Template(content)
        content = template.render_unicode()

        return content
