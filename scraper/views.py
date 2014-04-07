"""API views."""
import datetime

from flask import Blueprint

from scraper import const
from scraper import utils
from scraper import social
from scraper import cache

user_api = Blueprint('user_api', __name__)


@user_api.route("/api/users")
@utils.jsonify
def get_user(user_id=const.TWITTER, social_id=const.TWITTER, cache_time=-1):

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
    cache.get_engine().add_user(social_user.user_id, social_user.social_id,
                                social_user)

    return social_user
