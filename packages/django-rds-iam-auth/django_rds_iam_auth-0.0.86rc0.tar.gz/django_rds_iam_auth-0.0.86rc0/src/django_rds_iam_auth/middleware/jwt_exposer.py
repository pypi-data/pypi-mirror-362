import threading

from django.conf import settings

local = threading.local()


class JWTExposer(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        local.access_token = request.META.get('HTTP_AUTHORIZATION', None)
        local.id_token = request.META.get('HTTP_IDTOKEN', None)

        local.identity_pool_id = request.META.get('HTTP_IPI', None)
        local.user_pool_id = request.META.get('HTTP_UPI', None)
        local.tenant = request.META.get('HTTP_TTN', None)

        local.account_id = settings.AWS_ACCOUNT_ID
        local.user_id = None
        local.tenant_id = None
        local.id_token_payload = None
        local.access_token_payload = None

        if local.access_token and local.access_token.startswith("Bearer "):
            local.access_token = str.replace(local.access_token, 'Bearer ', '')

        response = self.get_response(request)
        return response
