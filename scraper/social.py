
from flask.ext.oauth import OAuth
from flask import app
from scraper import const

oauth2 = OAuth()

# CONSUMER_KEY = "tABdYJMuPkqlQ7G9Q9JQkyh25"
# CONSUMER_SECRET = "qEUkeXVDyqIgDGl6aZyIS18wVAyhnmU0XxEvNgVkf7UXfbbDa1"
#
# ACCESS_KEY = "2430801134-A7lrsPohAE0awA00CzH8P9rqbvTz9xDRSCQkG7r"
# ACCESS_SECRET = "DUmSjuYlnFuIaLwUi4i33NhILojrj172wLvmUBsgjXEwR"
#

class Social(object):

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

    def __init__(self, *args, **kwargs):
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
        @self.api.tokengetter
        def f():
            if not self.access_key and not self.access_secret:
                return None

            return self.access_key, self.access_secret

    def get_user(self, user_name):
        return dict(user_name=None, name=None)


class Twitter(Social):

    def __init__(self):
        self.name = const.TWITTER

        self.api_url = 'https://api.twitter.com/'
        self.request_token_url = 'https://api.twitter.com/oauth/request_token'
        self.access_token_url = 'https://api.twitter.com/oauth/access_token'
        self.authorize_url = 'https://api.twitter.com/oauth/authenticate'

        # get app.

        self.consumer_key = ""
        self.consumer_secret = CONSUMER_SECRET

        self.access_key = ACCESS_KEY
        self.access_secret = ACCESS_SECRET

        super(Twitter, self).__init__()

    def get_user(self, user_name):
        response = self.api.get('/1.1/users/show.json', data={'id': user_name})
        return response.data


class Facebook(Social):

    def __init__(self):
        self.name = const.FACEBOOK

        self.api_url = 'https://graph.facebook.com/'
        self.request_token_url = None
        self.access_token_url = '/oauth/access_token'
        self.authorize_url = 'https://www.facebook.com/dialog/oauth'

        self.consumer_key = "660159060688183"
        self.consumer_secret = "ca66655ba7801fabc8d52c10539d0660"

        # self.access_key = "d2c49bdbce48cda73a15ba3d9885dfd1"
        self.access_key = ''
        self.access_secret = ''

        super(Facebook, self).__init__(
            request_token_params={'scope': 'email'}
        )

        @self.api.authorized_handler
        def f(resp):
            self.access_key = resp['access_token']
            print self.access_key

    def get_user(self, user_name):
        response = self.api.get('/me/friends.json')
        return response.data
