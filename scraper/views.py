"""API views."""

from flask import Blueprint

from scraper import utils

user_api = Blueprint('user_api', __name__)


@user_api.route("/users")
@utils.jsonify
def get_user():
    return {}
