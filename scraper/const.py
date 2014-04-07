"""Generic package constants."""

FACEBOOK = 'facebook'
TWITTER = 'twitter'

SOCIALS = (TWITTER, FACEBOOK)

# Config *.ini file path as argument.
ARG_CONFIG_PATH = ("-c", "--config")

# Config *.ini file path as environment variable.
ENV_CONFIG_PATH = 'SCRAPER_CONFIG_PATH'


MAIL_USERNAME = "scraper.daemon"
MAIL_PASSWORD = "1Q2W3e4r"
MAIL_PROVIDER = "yandex.ru"

# Config *.ini file sections.
GENERAL_SECTION = 'general'

SOCIAL_SECTIONS = SOCIALS
CONFIG_SECTIONS = (GENERAL_SECTION,) + SOCIAL_SECTIONS



