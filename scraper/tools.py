"""Application manage tools."""

import logging

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from scraper import settings
from scraper import views


application = Flask(__name__)
db = SQLAlchemy()


class Tools(object):

    def _configure_app(self):
        # Set config.
        config = settings.Config()
        config.read()
        application.config.update(**config.to_flask())

        # Register views.
        application.register_blueprint(views.user_api)

        # Init caching engine.
        db.init_app(application)

    def init_db(self):
        """Initialize database schema."""
        self._configure_app()
        db.create_all()
        logging.info("Database schema was successfully initialized.")

    def drop_db(self):
        """Drop tables from the database."""
        self._configure_app()
        db.drop_all()
        logging.info("Database schema successfully dropped.")

    def reset_db(self):
        """Reset database schema (drop and init tables)."""
        self._configure_app()
        db.drop_all()
        db.create_all()
        logging.info("Database schema successfully reseted.")

    def run(self):
        """Run Flask development server."""
        self._configure_app()
        application.run()
