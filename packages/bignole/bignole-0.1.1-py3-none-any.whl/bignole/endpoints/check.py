#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""`check` command for bignole."""

import sys

import bignole.endpoints.common


class CheckApp(bignole.endpoints.common.App):  # pylint: disable-msg=missing-class-docstring
    def do(self):
        return self.output()


main = bignole.endpoints.common.main(CheckApp)

if __name__ == "__main__":
    sys.exit(main())
