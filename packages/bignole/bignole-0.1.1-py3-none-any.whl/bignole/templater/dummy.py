# -*- coding: utf-8 -*-
# pylint: disable-msg=missing-class-docstring,too-few-public-methods


class Templater:
    """The name of the templater to show."""

    name = "dummy"

    def render(self, content):
        """Use the template engine to render the SSH config"""
        return content
