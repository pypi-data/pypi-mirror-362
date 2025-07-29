import json
from typing import Union

import jwt
import requests
from django.urls import resolve
from django.conf import settings
from rest_framework import status
from django.core.cache import caches
from django.http import JsonResponse

from django_rds_iam_auth.middleware.jwt_exposer import local


class VerifyToken(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self.is_verification_required(request):
            try:
                self.pre_token_decoding_trigger(request)
                local.access_token_payload = self.decode_token(local.access_token)
                client_id = local.access_token_payload['client_id']
                local.id_token_payload = self.decode_token(local.id_token, client_id)
                local.user_id = local.access_token_payload['sub']
                self.post_token_decoding_trigger(request)
            except jwt.InvalidTokenError as e:
                if e.args[0] == 'Signature verification failed':
                    return self.invalid_token_response()
                elif e.args[0] == 'Signature has expired':
                    return self.token_expire_response()
                elif e.args[0] == 'Invalid payload padding':
                    return self.invalid_padding_response()
                elif e.args[0] == 'Invalid crypto padding':
                    return self.invalid_crypto_padding_response()
                elif e.args[0] in ('Invalid audience', "Audience doesn't match"):
                    return self.invalid_audience_response()
                elif e.args[0] == 'Not enough segments':
                    return self.not_enough_segments()
            except Exception:
                return self.failed_verify_response()
        else:
            local.access_token = None
            local.id_token = None

        response = self.get_response(request)
        return response

    def is_verification_required(self, request) -> bool:
        url_name = resolve(request.path_info).url_name
        return bool(
            not hasattr(settings, 'NON_SECURE_ROUTES') or url_name not in settings.NON_SECURE_ROUTES
            and not request.path_info.startswith('/admin')
            and not request.path_info.startswith('/manufacture')
        )

    def pre_token_decoding_trigger(self, request):
        pass

    def post_token_decoding_trigger(self, request):
        pass

    @staticmethod
    def cache_jwks_keys():
        all_keys = requests.get(settings.KEYS_URL).json().get('keys')
        if not all_keys:
            raise Exception("Failed to fetch keys")
        for key in all_keys:
            caches['default'].set(f'jwk_{key["kid"]}', key, timeout=60 * 60)

    @staticmethod
    def get_jwk(kid: str) -> dict:
        if key := caches['default'].get(f'jwk_{kid}', None):
            return key
        VerifyToken.cache_jwks_keys()
        return caches['default'].get(f'jwk_{kid}', None)

    @staticmethod
    def decode_token(token: str, audience: Union[str, None] = None) -> dict:
        header = jwt.get_unverified_header(token)
        jwk_value = VerifyToken.get_jwk(header['kid'])
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk_value))
        return jwt.decode(token, public_key, audience=audience, algorithms=['RS256'])

    @staticmethod
    def invalid_audience_response():
        return JsonResponse(
            data={'detail': 'Invalid audience'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def token_expire_response():
        return JsonResponse(
            data={'message': 'Token expired', 'code': 'Token expired'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    @staticmethod
    def invalid_padding_response():
        return JsonResponse(
            data={'detail': 'Invalid payload padding'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def invalid_crypto_padding_response():
        return JsonResponse(
            data={'detail': 'Invalid crypto padding'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    @staticmethod
    def invalid_token_response():
        return JsonResponse(
            data={'detail': 'Invalid token'},
            status=status.HTTP_403_FORBIDDEN,
        )

    @staticmethod
    def no_keys_response():
        return JsonResponse(
            data={'details': 'The JWKS endpoint does not contain any keys'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def access_token_is_missing_response():
        return JsonResponse(
            data={'detail': 'Access token missing'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def id_token_is_missing_response():
        return JsonResponse(
            data={'details': 'Id token missing'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def tokens_are_missing_response():
        return JsonResponse(
            data={'details': 'Access and id tokens are missing'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def not_enough_segments():
        return JsonResponse(
            data={'detail': 'Not enough segments'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    def failed_verify_response():
        return JsonResponse(
            data={'detail': 'Failed to verify token'},
            status=status.HTTP_403_FORBIDDEN,
        )
