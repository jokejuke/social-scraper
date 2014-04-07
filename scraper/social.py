import datetime

from flask import current_app
from flask.ext.oauth import OAuth
from scraper import const
from scraper import utils


oauth2 = OAuth()


class User(utils.ADict):
    """Holds app specified user to got from social or cache."""

    attrs = (
        ('user_id', str, None),
        ('social_id', str, None),

        ('name', str, None),
        ('popularity', int, None),
        # ('updated_at', datetime.datetime, datetime.datetime.now()),
        ('cached', bool, False),
    )

    def __init__(self, *args, **kwargs):
        super(User, self).__init__()

        # Update defaults according to given args and kwargs.
        arguments = dict(*args, **kwargs)

        for name, typ, default in self.attrs:
            value = arguments.get(name)
            self[name] = default if value is None else typ(value)


class _Social(object):

    # Application name
    name = None

    # Consumer (application) and access token
    consumer_key = ""
    consumer_secret = ""
    access_key = ""
    access_secret = ""

    # API url
    api_url = "https://api.example.com/"

    # Look for new request tokens
    request_token_url = "https://api.example.com/"

    # Exchange token with the remote application
    access_token_url = "https://api.example.com/"

    # Authorization url
    authorize_url = 'https://api.example.com/oauth/authenticate'

    config_attrs = ('consumer_key', 'consumer_secret',
                    'access_key', 'access_secret')

    def __init__(self, *args, **kwargs):
        for attr in self.config_attrs:
            setattr(self, attr, current_app.config[self.name].get(attr))

        self.api = oauth2.remote_app(
            self.name,
            base_url=self.api_url,
            request_token_url=self.request_token_url,
            access_token_url=self.access_token_url,
            authorize_url=self.authorize_url,

            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,

            *args,
            **kwargs
        )

        self.api.tokengetter(self._get_token)

    def _get_token(self):
        if not self.access_key and not self.access_secret:
            return None

        return self.access_key, self.access_secret

    def get_user(self, username):
        """Return User instance got from social."""
        return User(user_id=username, social_id=self.name)


class Twitter(_Social):

    def __init__(self):
        self.name = const.TWITTER

        self.api_url = 'https://api.twitter.com/'
        self.request_token_url = 'https://api.twitter.com/oauth/request_token'
        self.access_token_url = 'https://api.twitter.com/oauth/access_token'
        self.authorize_url = 'https://api.twitter.com/oauth/authenticate'

        super(Twitter, self).__init__()

    def get_user(self, username):
        response = self.api.get('/1.1/users/show.json', data={'id': username})

        user = super(Twitter, self).get_user(username)
        user.name = response.data['name']
        user.popularity = response.data['followers_count']

        return user


class Facebook(_Social):

    def __init__(self):
        self.name = const.FACEBOOK

        self.api_url = 'https://graph.facebook.com/'
        self.request_token_url = None
        self.access_token_url = '/oauth/access_token'
        self.authorize_url = 'https://www.facebook.com/dialog/oauth'

        super(Facebook, self).__init__(
            request_token_params={'scope': 'email'}
        )

        @self.api.authorized_handler
        def f(resp):
            self.access_key = resp['access_token']
            print self.access_key

    def get_user(self, user_name):
        response = self.api.get('/me')
        return response.data


def get_engine(social_id, _engine_map=dict()):
    """Return dictionary with mapped socials."""
    if not _engine_map:
        _engine_map = {
            const.TWITTER: Twitter,
            const.FACEBOOK: Facebook,
        }

    return _engine_map.get(social_id)




