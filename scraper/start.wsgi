import os
import sys

# Dynamically add package to python path if it's not found.
ROOT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
if ROOT_PATH not in sys.path:
    sys.path.append(ROOT_PATH)

# Reintroduce application variable to pass WSGI env variables.
def application(environ, start_response):
    from scraper import start

    os.environ.setdefault(const.ENV_CONFIG_PATH,
                          environ.get(const.ENV_CONFIG_PATH))
    start.configurate()
    start.register()

    return start.application(environ, start_response)


