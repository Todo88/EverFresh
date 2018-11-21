# from social_core.backends.oauth import BaseOAuth2
#
#
# class IntuitOAuth2(BaseOAuth2):
#     """Intuit OAuth authentication backend"""
#     name = 'intuit'
#     AUTHORIZATION_URL = 'https://appcenter.intuit.com/connect/oauth2'
#     ACCESS_TOKEN_URL = 'https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer'
#     SCOPE_SEPARATOR = ','
# EXTRA_DATA = [
#     ('id', 'id'),
#     ('expires', 'expires')
# ]

# def get_user_details(self, response):
#     """Return user details from GitHub account"""
#     return {'username': response.get('login'),
#             'email': response.get('email') or '',
#             'first_name': response.get('name')}
#
# def user_data(self, access_token, *args, **kwargs):
#     """Loads user data from service"""
#     url = 'https://api.github.com/user?' + urlencode({
#         'access_token': access_token
#     })
#     return self.get_json(url)


class OAuth2Config:
    def __init__(self, issuer='', auth_endpoint='', token_endpoint='', userinfo_endpoint='', revoke_endpoint='',
                 jwks_uri=''):
        self.issuer = issuer
        self.auth_endpoint = auth_endpoint
        self.token_endpoint = token_endpoint
        self.userinfo_endpoint = userinfo_endpoint
        self.revoke_endpoint = revoke_endpoint
        self.jwks_uri = jwks_uri
