import jwt
from django.conf import settings
from django_rds_iam_auth.middleware.jwt_exposer import local


class JWTInjector(object):

    def __call__(self, **kwargs):
        # user_data = jwt.decode(id_token, verify=False)
        if 'IdToken' not in kwargs or 'AccessToken' not in kwargs or 'IPI' not in kwargs or 'UPI' not in kwargs:
            raise Exception('missing information')
        local.access_token = kwargs['AccessToken']
        local.id_token = kwargs['IdToken']
        local.identity_pool_Id = kwargs['IPI']
        local.user_pool_id = kwargs['UPI']
        local.tenant = kwargs['ttn']
        local.account_id = settings.AWS_ACCOUNT_ID
