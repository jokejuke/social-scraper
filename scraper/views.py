"""API views."""
import datetime

# from flask import Blueprint
from flask.ext.restful import abort
from flask.ext.restful import Resource
from flask.ext.restful import reqparse

from scraper import const
from scraper import utils
from scraper import social
from scraper import cache
from scraper.tools import api


class User(Resource):

    def __init__(self):
        self._get_parser = reqparse.RequestParser()
        self._get_parser.add_argument('user_id', type=str,
                                      help='User name (login) or user id')
        self._get_parser.add_argument('social_id', type=str,
                                      help='Social backend. One from {0}'
                                      .format(const.SOCIALS))
        self._get_parser.add_argument('cache_time', type=int,
                                      help='Max age of the cached data')

    @utils.jsonify
    def get(self):
        args = self._get_parser.parse_args()
        user_id = args.get('user_id') or const.TWITTER
        social_id = args.get('social_id') or const.TWITTER
        cache_time = args.get('cache_time') or -1

        if social_id not in const.SOCIALS:
            return dict()

        # Get user from cache.
        cached_user = cache.get_engine().get_user(user_id, social_id)
        if cached_user is not None:
            cached_time = datetime.datetime.now() - cached_user.updated_at
            cached_time = int(cached_time.total_seconds())

            if cache_time == -1 or cache_time >= cached_time:
                return cached_user

        # Get user from social API.
        social_user = social.get_engine(social_id).get_user(user_id)
        if social_user is not None:
            cache.get_engine().add_user(social_user.user_id,
                                        social_user.social_id,
                                        social_user)

            return social_user
        else:
            abort(404, message="User '{0}' in social '{1}' not found"
                  .format(user_id, social_id))


class UserList(Resource):

    @utils.jsonify
    def get(self):
        """Get all users from cache."""
        cached_users = cache.get_engine().get_users()
        return cached_users


api.add_resource(UserList, '/api/users/')
api.add_resource(User, '/api/user/')
