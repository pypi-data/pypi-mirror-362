import time

import jwt

from django.contrib.auth.models import AnonymousUser
from rest_framework import authentication

from jsm_user_services.drf_tools.exceptions import InvalidToken as CustomInvalidToken
from jsm_user_services.drf_tools.exceptions import NotAuthenticated as CustomNotAuthenticated
from jsm_user_services.services.user import current_jwt_token
from jsm_user_services.support.auth_jwt import get_decoded_oauth_token


class OauthJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = current_jwt_token()
        if token is None:
            raise CustomNotAuthenticated()

        try:
            payload = get_decoded_oauth_token(token)
            current_timestamp = int(time.time())
            is_token_expired = "exp" in payload and current_timestamp > payload["exp"]
            is_sub_claim_in_payload = "sub" in payload
            if not is_token_expired and is_sub_claim_in_payload:
                return (AnonymousUser(), token)
            else:
                raise CustomInvalidToken()
        except jwt.DecodeError:
            raise CustomInvalidToken()
