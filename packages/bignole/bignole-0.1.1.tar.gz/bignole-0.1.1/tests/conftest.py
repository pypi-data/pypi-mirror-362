# -*- coding: utf-8 -*-


import os
import os.path
import shutil
import sys
import unittest.mock

import inotify_simple
import pytest

import bignole
import bignole.templater


def have_mocked(request, *mock_args, **mock_kwargs):
    if len(mock_args) > 1:
        method = unittest.mock.patch.object
    else:
        method = unittest.mock.patch

    patch = method(*mock_args, **mock_kwargs)
    mocked = patch.start()

    request.addfinalizer(patch.stop)

    return mocked


@pytest.fixture
def no_sleep(monkeypatch):
    monkeypatch.setattr("time.sleep", lambda arg: arg)


@pytest.fixture
def mock_get_content(request):
    return have_mocked(request, "bignole.utils.get_content")


@pytest.fixture(scope="session", autouse=True)
def mock_logger(request):
    return have_mocked(request, "bignole.utils.logger")


@pytest.fixture(autouse=True)
def mock_log_configuration(request):
    have_mocked(request, "socket.socket")  # required for SysLogHandler

    marker = request.node.get_closest_marker("no_mock_log_configuration")

    if not marker:
        return have_mocked(request, "bignole.utils.configure_logging")


@pytest.fixture
def ptmpdir(request, tmpdir):
    for key in "TMP", "TEMPDIR", "TEMP":
        os.environ[key] = tmpdir.strpath

    request.addfinalizer(lambda: shutil.rmtree(tmpdir.strpath))

    return tmpdir


@pytest.fixture
def sysargv(monkeypatch):
    argv = ["bignole"]

    monkeypatch.setattr(sys, "argv", argv)

    return argv


@pytest.fixture
def inotifier(request):
    mock = have_mocked(request, "inotify_simple.INotify")
    mock.return_value = mock
    mock.__enter__.return_value = mock

    values = [inotify_simple.Event(0, 0, 0, os.path.basename(bignole.DEFAULT_RC))]
    values *= 3

    def side_effect():
        if values:
            return [values.pop()]
        raise KeyboardInterrupt

    mock.read.side_effect = side_effect
    mock.v = values

    return mock


@pytest.fixture
def template_render(request):
    return have_mocked(request, bignole.templater.Templater, "render")


@pytest.fixture(params=(None, "-d", "--debug"))
def cliparam_debug(request):
    return request.param


@pytest.fixture(params=(None, "-v", "--verbose"))
def cliparam_verbose(request):
    return request.param


@pytest.fixture(params=(None, "-s", "--source-path"))
def cliparam_source_path(request):
    return request.param


@pytest.fixture(params=(None, "-o", "--destination-path"))
def cliparam_destination_path(request):
    return request.param


@pytest.fixture(params=(None, "-b", "--boring-syntax"))
def cliparam_boring_syntax(request):
    return request.param


@pytest.fixture(params=(None, "-a", "--add-header"))
def cliparam_add_header(request):
    return request.param


@pytest.fixture(params=(None, "--systemd"))
def cliparam_systemd(request):
    return request.param


@pytest.fixture(params=(None, "--pipesh"))
def cliparam_pipesh(request):
    return request.param


@pytest.fixture
def cliargs_default(sysargv):
    return sysargv


@pytest.fixture
def cliargs_fullset(
    sysargv,
    cliparam_debug,
    cliparam_verbose,
    cliparam_source_path,
    cliparam_destination_path,
    cliparam_boring_syntax,
    cliparam_add_header,
):
    options = {
        "debug": cliparam_debug,
        "verbose": cliparam_verbose,
        "source_path": cliparam_source_path,
        "destination_path": cliparam_destination_path,
        "add_header": cliparam_add_header,
        "boring_syntax": cliparam_boring_syntax,
    }
    bool_params = (
        cliparam_debug,
        cliparam_verbose,
        cliparam_boring_syntax,
        cliparam_add_header,
    )
    value_params = (cliparam_source_path, cliparam_destination_path)

    for param in bool_params:
        if param:
            sysargv.append(param)

    for param in value_params:
        if param:
            sysargv.append(param)
            sysargv.append("/path/to")

    return sysargv, options


@pytest.fixture
def cliargs_bignole_fullset(cliargs_fullset, cliparam_systemd, cliparam_pipesh):
    sysargv, options = cliargs_fullset

    for param in cliparam_systemd, cliparam_pipesh:
        if param:
            sysargv.append(param)

    options["systemd"] = cliparam_systemd
    options["pipesh"] = cliparam_pipesh

    return sysargv, options


@pytest.fixture
def mock_mainfunc(cliargs_default, mock_get_content, inotifier):
    # pylint: disable-msg=R0801
    mock_get_content.return_value = """\
Compression yes

Host q
    HostName e

    Host b
        HostName lalala
    """

    return cliargs_default, mock_get_content, inotifier
