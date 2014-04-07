"""Application manage tools."""

import logging

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from scraper import settings
from scraper import views


application = Flask(__name__)
db = SQLAlchemy(__name__)


def init_db(self):
    """Initialize database schema."""
    db.metadata.create_all(db.engine)
    logging.info("Database schema was successfully initialized.")


def drop_db(self):
    """Drop tables from the database."""
    db.drop_all(db.engine)
    logging.info("Database schema successfully dropped.")


def reset_db(self):
    """Reset database schema (drop and init tables)."""
    self.drop_db()
    self.init_db()


def _configure(config_path=None):
    config = settings.Config()
    config.read(config_path)
    application.config.update(**config.to_flask())


def _register():
    application.register_blueprint(views.user_api)


def runserver():
    """Run Flask development server."""
    _configure()
    _register()

    application.run()
