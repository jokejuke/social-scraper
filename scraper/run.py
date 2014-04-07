#!/home/y/bin/python2.6

"""Backend CLI."""

import argparse
import logging
import os
import sys

# Dynamically add package to python path if it's not found to allow to run
# module from anywhere without caring about it's location.
ROOT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
if ROOT_PATH not in sys.path:
    sys.path.append(ROOT_PATH)

from scraper import const

# from scraper import tools
from scraper import start


def _init_parser():
    parser = argparse.ArgumentParser(
        description="%s. %s" % ("""Social Scraper""", __doc__),
    )
    parser.add_argument(
        *const.ARG_CONFIG_PATH,
        metavar="<config-file>",
        required=True,
        type=str,
        dest="config",
        help="Configuration ini file"
    )
    subparsers = parser.add_subparsers(
        help='List of available database actions',
        dest='action'
    )

    def _add_action(func):
        helpstring = filter(None, func.__doc__.split('\n'))[0]
        subparser = subparsers.add_parser(func.__name__, help=helpstring)
        subparser.set_defaults(func=func)

    # db_tools = tools.DBTools()

    # _add_action(db_tools.init)
    # _add_action(db_tools.drop)
    # _add_action(db_tools.reset)
    _add_action(start.runserver)

    return parser


def run_cli():
    """Run CLI interface."""
    try:
        # TODO: finish db tools handling.

        # Parsing
        parser = _init_parser()
        args = parser.parse_args()

        # Call function.
        os.environ.setdefault(const.ENV_CONFIG_PATH, args.config)
        args.func()

    except Exception as e:
        logging.exception("Unknown internal error, see the trace below.")
        return -1

if __name__ == "__main__":
    exit(run_cli())
