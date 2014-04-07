"""Caching database models."""


from flask import app
from scraper.tools import db

class AlchemyCache(db.Model):
    __tablename__ = "social_user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    socialname = db.Column(db.String)
    popularity = db.Column(db.Integer)

    created = db.Column(db.Date)
    updated = db.Column(db.Date)
    removed = db.Column(db.Boolean)

    def __init__(self, username, socialname, popularity):
        self.username = username
        self.socialname = socialname
        self.popularity = popularity

    @staticmethod
    def get_or_create(username, socialname, popularity):
        user = AlchemyCache.query.filter_by(username=username, socialname=socialname).first()
        if user is None:
            user = AlchemyCache(username, socialname, popularity)
            db.session.add(user)
            db.session.commit()
        return user
