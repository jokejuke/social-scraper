"""Settings module with global variables."""

import ConfigParser
import logging
import os

from scraper import const


class NonEmptyConfigParser(ConfigParser.SafeConfigParser):
    """Print warning for empty options in the config."""

    def get(self, section, option):
        value = ConfigParser.SafeConfigParser.get(self, section, option)

        if value:
            value = value.strip()

        if len(value) == 0:
            msg = ("Section '{0}' and option '{1}' has an (likely invalid) "
                   "empty value!".format(section, option))
            logging.warn(msg)
        return value


class Config(object):
    """Holds reading and parsing of the configuration files (.ini, etc.)"""

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

            # General settings.
            if section == const.GENERAL_SECTION:
                opts = (
                    ('debug', bool),
                    ('secret_key', str),
                    ('cache_engine', str),
                    ('cache_uri', str),
                    ('cache_debug', bool),
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

        return self._dashboard

    def read(self, path=None):
        """Read settings from .ini file with path."""

        path = path or self._path or os.environ.get(const.ENV_CONFIG_PATH)

        # Raised in case if path does not specified anywhere.
        if path is None:
            msg = (
                "Path to config file does not specified neither as parameter "
                "{0} nor as environment variable {1}"
                .format(const.ARG_CONFIG_PATH, const.ENV_CONFIG_PATH)
            )
            raise ConfigParser.Error(msg)

        if not os.path.exists(path) or not os.access(path, os.R_OK):
            raise ConfigParser.Error(
                "Configuration file '{0}' not found or cannot be read."
                .format(path)
            )

        read_ok = self._parser.read(path)
        if not read_ok:
            raise ConfigParser.Error("Cannot read config file '{0}'."
                                     .format(path))

        return self._get()

    def to_flask(self):
        """Return dictionary suitable to set into Flask application config."""

        return {
            # App global opts.
            'DEBUG': self._dashboard[const.GENERAL_SECTION]['debug'],
            'SECRET_KEY': self._dashboard[const.GENERAL_SECTION]['secret_key'],
            'CACHE_ENGINE': self._dashboard[const.GENERAL_SECTION]['cache_engine'],
            'SQLALCHEMY_DATABASE_URI': self._dashboard[const.GENERAL_SECTION]['cache_uri'],
            'SQLALCHEMY_ECHO': self._dashboard[const.GENERAL_SECTION]['cache_debug'],

            # Socials opts.
            const.TWITTER: self._dashboard[const.TWITTER],
            const.FACEBOOK: self._dashboard[const.FACEBOOK],
        }
