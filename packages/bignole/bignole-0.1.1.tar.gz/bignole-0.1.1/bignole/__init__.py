# -*- coding: utf-8 -*-
import os.path
import warnings


VERSION = "0.1.1"


HOME_DIR = os.path.expanduser("~")
DEFAULT_RC = os.path.join(HOME_DIR, ".bignolerc")
DEFAULT_SSHCONFIG = os.path.join(HOME_DIR, ".ssh", "config")


warnings.simplefilter("always", DeprecationWarning)
