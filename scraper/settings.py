"""Settings module with global variables."""

import ConfigParser
import logging
import os
import sys

from scraper import const


class Error(ConfigParser.Error):
    """Holds typical errors when reading / parsing config file."""


class NotFoundError(Error):
    """Raised if config path not found."""

    def __init__(self, *args, **kwargs):
        error = (
            "Path to config file does not specified neither as parameter %s "
            "nor as environment variable %s" %
            (const.ARG_CONFIG_PATH, const.ENV_CONFIG_PATH)
        )
        super(NotFoundError, self).__init__(error)


class SectionValueError(Error):
    """Raised if given invalid section name."""

    def __init__(self, section_name):
        error = (
            "Section %s is in valid. Should be one of the predefined %s"
            % (section_name, const.CONFIG_SECTIONS)
        )
        super(SectionValueError, self).__init__(error)


class NonEmptyConfigParser(ConfigParser.SafeConfigParser):

    def get(self, section, option):
        value = ConfigParser.SafeConfigParser.get(self, section, option)

        if value:
            value = value.strip()

        if len(value) == 0:
            msg = ("Section '{0}' and option '{1}' has an disallowed "
                   "(and likely invalid) empty value!".format(section, option))
            logging.warn(msg)
        return value


class Config(object):

    def __init__(self, path=None):
        self._parser = NonEmptyConfigParser()
        self._dashboard = dict()
        self._path = path

        self._get_methods = {
            str: self._parser.get,
            bool: self._parser.getboolean,
            int: self._parser.getint,
            float: self._parser.getfloat
        }

        self._db_opts = dict()
        self._general_opts = dict()

    def _get_section(self, section, opts):
        for opt_name, opt_type in opts:
            opt_value = self._get_methods[opt_type](section, opt_name)
            self._dashboard[section][opt_name] = opt_value

    def _get(self):
        """
        Parse and return parsed settings from .ini file according to specified
        section.
        """

        for section in const.CONFIG_SECTIONS:
            self._dashboard[section] = dict()
            try:
                # General settings.
                if section == const.GENERAL_SECTION:
                    opts = (
                        ('debug', bool),
                        ('secret_key', str),
                        ('cache_backend', str),
                        ('cache_uri', str),
                    )
                    self._get_section(section, opts)

                # Socials settings.
                elif section in const.SOCIAL_SECTIONS:

                    opts = (
                        ('consumer_key', str),
                        ('consumer_secret', str),
                        ('access_key', str),
                        ('access_secret', str),
                    )
                    self._get_section(section, opts)

            except ConfigParser.Error as e:
                raise Error(e), None, sys.exc_info()[-1]

        return self._dashboard

    def read(self, path=None):
        """Read settings from .ini file with path."""

        path = path or self._path or os.environ.get(const.ENV_CONFIG_PATH)

        # Raised in case if path does not specified anywhere.
        if path is None:
            raise NotFoundError()

        if not os.path.exists(path) or not os.access(path, os.R_OK):
            raise Error("Configuration file '%s' not found or cannot be read."
                        % path)
        try:
            read_ok = self._parser.read(path)
        except ConfigParser.Error as e:
            raise Error(e), None, sys.exc_info()[-1]
        else:
            if not read_ok:
                raise Error("Cannot read config file '%s'." % path)

        return self._get()

    def to_flask(self):

        return {
            'DEBUG': self._dashboard[const.GENERAL_SECTION]['debug'],
            'SECRET_KEY': self._dashboard[const.GENERAL_SECTION]['secret_key'],
            'SQLALCHEMY_DATABASE_URI': self._dashboard[const.GENERAL_SECTION]['cache_uri'],
        }

    @property
    def dashboard(self):
        return self._dashboard
