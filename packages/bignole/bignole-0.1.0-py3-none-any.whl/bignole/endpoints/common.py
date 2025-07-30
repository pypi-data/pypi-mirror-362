# -*- coding: utf-8 -*-
# pylint: disable-msg=missing-function-docstring


import abc
import os

import bignole.core.processor
import bignole.endpoints.cli
import bignole.endpoints.templates
import bignole.templater
import bignole.utils


LOG = bignole.utils.logger(__name__)


class App(metaclass=abc.ABCMeta):  # pylint: disable-msg=missing-class-docstring
    @classmethod
    def specify_parser(cls, parser):
        return parser

    def __init__(self, options):
        self.source_path = options.source_path
        self.destination_path = options.destination_path
        self.boring_syntax = options.boring_syntax
        self.add_header = options.add_header
        self.templater_name = options.use_templater

        try:
            self.templater = bignole.templater.resolve_templater(self.templater_name)
        except KeyError as exc:
            raise ValueError(
                f"Cannot find templater for {options.use_templater}"
            ) from exc

        if self.add_header is None:
            self.add_header = options.destination_path is not None

        bignole.utils.configure_logging(
            options.debug, options.verbose, self.destination_path is None
        )

    @abc.abstractmethod
    def do(self):
        pass

    def output(self):
        """Write ssh config to file or to STDOUT"""
        content = self.get_new_config()

        if self.destination_path is None:
            print(content)
            return

        try:
            with bignole.utils.topen(self.destination_path, True) as destfp:
                destfp.write(content)
        except Exception as exc:
            self.log_error("Cannot write to file %s: %s", self.destination_path, exc)
            raise

    def get_new_config(self):
        content = self.fetch_content()

        if self.templater_name:
            content = self.apply_template(content)
        else:
            LOG.info("No templating is used.")

        if not self.boring_syntax:
            content = self.process_syntax(content)
        else:
            LOG.info("Boring syntax was choosen, not processing is applied.")

        if self.add_header:
            content = self.attach_header(content)
        else:
            LOG.info("No need to attach header.")

        return content

    def fetch_content(self):
        LOG.info("Fetching content from %s", self.source_path)

        try:
            content = bignole.utils.get_content(self.source_path)
        except Exception as exc:
            self.log_error("Cannot fetch content from %s: %s", self.source_path, exc)
            raise

        LOG.info("Original content of %s:\n%s", self.source_path, content)

        return content

    def apply_template(self, content):
        LOG.info("Applying templater to content of %s.", self.source_path)

        try:
            content = self.templater.render(content)
        except Exception as exc:
            self.log_error(
                "Cannot process template (%s) in source file %s.",
                self.source_path,
                self.templater.name,
                exc,
            )
            raise

        LOG.info("Templated content of %s:\n%s", self.source_path, content)

        return content

    def process_syntax(self, content):
        try:
            return bignole.core.processor.process(content)
        except Exception as exc:
            self.log_error(
                "Cannot parse content of source file %s: %s", self.source_path, exc
            )
            raise

    def attach_header(self, content):
        """Add header at the beginning of the config"""
        header = bignole.endpoints.templates.make_header(rc_file=self.source_path)
        content = header + content

        return content

    def log_error(self, template, *args):
        LOG.error(template, *args)


def main(app_class):
    def main_func():  # pylint: disable-msg=inconsistent-return-statements
        parser = bignole.endpoints.cli.create_parser()
        parser = app_class.specify_parser(parser)
        options = parser.parse_args()
        app = app_class(options)

        LOG.debug("Options: %s", options)

        try:
            return app.do()
        except KeyboardInterrupt:
            pass
        except Exception as exc:  # pylint: disable-msg=broad-exception-caught
            LOG.exception("Failed with error %s", exc)
            return os.EX_SOFTWARE

    return main_func
