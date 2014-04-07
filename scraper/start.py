from flask import Flask

from scraper import settings
from scraper import views

application = Flask(__name__)
db = Flask(__name__)


def configurate(config_path=None):
    config = settings.Config()
    config.read(config_path)
    application.config.update(**config.to_flask())


def register():
    application.register_blueprint(views.user_api)


def runserver():
    """Run Flask development server."""
    configurate()
    register()

    application.run()
