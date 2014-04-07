"""API views."""

from flask import Blueprint
from flask import request

from scraper import utils

user_api = Blueprint('user_api', __name__)

@user_api.route("/user/<username><social>")
@utils.jsonify
def get_user(username, social):

    name = request.values.get('query', u"")
    return {}
