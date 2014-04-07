"""Caching database models."""

import datetime

from flask import current_app

from scraper import const
from scraper import social
from scraper.tools import db


class AlchemyCache(db.Model):
    """SQLAlchemy based cache engine."""

    __tablename__ = "social_user"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String)
    social_id = db.Column(db.String)

    name = db.Column(db.String)
    popularity = db.Column(db.Integer)

    updated_at = db.Column(db.DateTime)

    # TODO : use removed_at field when user left in cache but removed in source
    # removed_at = db.Column(db.DateTime)

    def __init__(self, user_id, social_id, name=None, popularity=None):
        self.user_id = user_id
        self.social_id = social_id
        self.name = name
        self.popularity = popularity
        self.updated_at = datetime.datetime.now()

    @classmethod
    def get_user(cls, user_id, social_id):
        user = None

        query = cls.query.filter_by(user_id=user_id, social_id=social_id)
        cache_user = query.first()
        if cache_user:
            user = social.User(
                user_id=cache_user.user_id,
                social_id=cache_user.social_id,
                name=cache_user.name,
                popularity=cache_user.popularity,
                updated_at=cache_user.updated_at,
                cached=True
            )

        return user

    @classmethod
    def add_user(cls, user_id, social_id, user):

        query = cls.query.filter_by(user_id=user_id, social_id=social_id)
        cache_user = query.first()

        if not cache_user:
            cache_user = cls(user_id, social_id, user.name, user.popularity)
            db.session.add(cache_user)
            db.session.commit()
            return user, True

        else:
            cache_user.name = user.name
            cache_user.popularity = user.popularity
            cache_user.updated_at = datetime.datetime.now()
            db.session.commit()
            return user, False


class RedisCache(object):
    """Redis based cache engine."""


def get_engine(_engine_map={}):
    """Return dictionary with mapped cache backends."""
    if not _engine_map:
        _engine_map = {
            const.SQLALCHEMY: AlchemyCache,
            const.REDIS: RedisCache,
        }
    return _engine_map.get(current_app.config[const.CACHE])





