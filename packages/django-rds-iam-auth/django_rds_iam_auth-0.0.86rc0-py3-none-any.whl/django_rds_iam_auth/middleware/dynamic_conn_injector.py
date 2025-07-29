import boto3
from rest_framework import status
from django.db import connections
from django.http import JsonResponse
from django.core.handlers.wsgi import WSGIRequest

from django_rds_iam_auth.middleware.jwt_exposer import local
from django_rds_iam_auth.utils import is_useful, create_connection
from django_rds_iam_auth.aws.utils.aws_access_heper import CredentialsManager


class ConnectionInjector(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not local.user_id:
            return self.get_response(request)
        try:
            dynamic_database = (
                connections.databases[local.user_id]
                if connections.databases.get(local.user_id)
                else connections.databases['default'].copy()
            )
            cred_manager = CredentialsManager(
                access_token=local.access_token,
                id_token=local.id_token,
                id_token_payload=local.id_token_payload,
                # Maybe it's make sense to ignore cognito user pool and identity pool from headers
                user_pool_id=local.user_pool_id,
                identity_pool_id=local.identity_pool_id,
            )
            credentials = local.credentials = cred_manager.get_credentials()
            # rds_boto3_session = boto3.session.Session(**credentials)
            # Potentially it's possible to update boto3 default session and create client from it
            # boto3.DEFAULT_SESSION = rds_boto3_session
            # rds_client = boto3.DEFAULT_SESSION.resource("rds")
            # rds_client = rds_boto3_session.client("rds", **credentials)
            # dynamic_database['id'] = local.user_id
            # dynamic_database['USER'] = local.user_id
            # dynamic_database['ENGINE'] = 'django_rds_iam_auth.aws.postgresql'
            # dynamic_database['PASSWORD'] = rds_client.generate_db_auth_token(
            #     DBHostname=dynamic_database['HOST'],
            #     Port=dynamic_database.get("port", 5432),
            #     DBUsername=local.user_id,
            # )
            connections.databases[local.user_id] = create_connection(dynamic_database, local.user_id, credentials)
            if not is_useful(local.user_id):
                cred_manager.reset_credentials()
                credentials = local.credentials = cred_manager.get_credentials()
                connections.databases[local.user_id] = create_connection(dynamic_database, local.user_id, credentials)
                is_useful(local.user_id, raise_exception=True)
        except Exception as e:
            return self.error_response(f'Failed to create rds connection. {e}')
        response = self.get_response(request)
        self.clean_local()
        return response

    @staticmethod
    def clean_local():
        local.user_id = None
        local.id_token_payload = None
        local.credentials = None
        local.access_token = None
        local.id_token = None
        local.tenant_id = None
        local.identity_pool_id = None
        local.user_pool_id = None

    def process_exception(self, request: WSGIRequest, exception: Exception) -> None:
        self.clean_local()

    @staticmethod
    def error_response(error_message: str) -> JsonResponse:
        return JsonResponse(data={'detail': error_message}, status=status.HTTP_400_BAD_REQUEST)
