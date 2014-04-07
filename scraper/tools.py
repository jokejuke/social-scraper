"""Application manage tools."""

import logging

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()


class Tools(object):

    def _configure_app(self):
        # Set config.
        from scraper import settings
        from scraper import views

        config = settings.Config()
        config.read()
        app.config.update(**config.to_flask())

        # Register views.
        app.register_blueprint(views.user_api)

        # Init caching engine.
        db.init_app(app)

    def init_db(self):
        """Initialize database schema."""
        self._configure_app()
        with app.app_context():
            db.create_all()
            logging.info("Database schema was successfully initialized.")

    def drop_db(self):
        """Drop tables from the database."""
        self._configure_app()
        with app.app_context():
            db.drop_all()
            logging.info("Database schema successfully dropped.")

    def reset_db(self):
        """Reset database schema (drop and init tables)."""
        self._configure_app()
        with app.app_context():
            db.drop_all()
            db.create_all()
            logging.info("Database schema successfully reseted.")

    def run(self):
        """Run Flask development server."""
        self._configure_app()
        app.run()
