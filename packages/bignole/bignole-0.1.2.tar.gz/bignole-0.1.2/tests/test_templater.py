# -*- coding: utf-8 -*-


import pytest

from bignole import templater
from bignole.templater import dummy


def test_all_templaters():
    tpls = templater.all_templaters()
    print(tpls)

    assert len(tpls) == 3
    assert tpls["dummy"] is dummy.Templater
    assert tpls["mako"]().render("<% a = 'mako' %>${a} q") == "mako q"
    assert tpls["jinja"]().render("{%- set a = 'jinja' -%}{{ a }} q") == "jinja q"


def test_resolve_templater_none():
    tpl = templater.resolve_templater("dummy")

    assert isinstance(tpl, dummy.Templater)
    assert tpl.name == "dummy"


def test_resolve_templater_default():
    assert templater.resolve_templater(None).name == "mako"

    assert (
        templater.resolve_templater(None, ["jinja", "mako", "dummy"]).name == "jinja2"
    )

    assert templater.resolve_templater(None, []).name == "dummy"


@pytest.mark.parametrize("code", ("mako", "jinja", "dummy"))
def test_resolve_templater_known(code):
    if code != "jinja":
        assert templater.resolve_templater(code).name == code
    else:
        assert templater.resolve_templater(code).name == "jinja2"


def test_render_dummy_templater():
    tpl = dummy.Templater()

    assert tpl.render("lalala") == "lalala"
