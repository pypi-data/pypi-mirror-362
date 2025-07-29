import logging
import datetime

import boto3
from dateutil.tz import tzlocal
from django.conf import settings
from django.core.cache import caches

logger = logging.getLogger('connection_injector')


class CredentialsManager:

    def __init__(
            self,
            access_token: str,
            id_token: str,
            id_token_payload: dict,
            identity_pool_id: str = settings.AWS_COGNITO_IDENTITY_POOL_ID,
            user_pool_id: str = settings.AWS_COGNITO_USER_POOL_ID,
    ) -> None:
        self._cache = caches['token_cache']
        self._access_token = access_token
        self._id_token = id_token
        self._identity_pool_id = identity_pool_id
        self._user_pool_id = user_pool_id
        self._id_token_payload = id_token_payload

    def get_credentials(self) -> dict:
        """
        get_credentials retrieves valid AWS credentials for the user associated with
        this CredentialsManager instance.

        It first checks if there are cached credentials associated with the access
        token. If so, it returns the cached credentials.

        If no cached credentials are found, it calls _fetch_credentials to retrieve
        new credentials, caches them, and returns them.

        The credentials returned will be a dict with keys for 'aws_access_key_id',
        'aws_secret_access_key', and 'aws_session_token'.

        Returns:
            dict: The AWS credentials dict containing AccessKeyId, SecretKey,
                  and SessionToken

        """
        credentials = self._cache.get(self._access_token, None)
        if not credentials or not isinstance(credentials, dict):
            logger.info("ConnectionInjector middleware: no cached credentials")
            credentials = self._fetch_credentials()
            logger.info(f"ConnectionInjector middleware: new credentials {credentials}")
        else:
            logger.info(f"ConnectionInjector middleware: using cached credentials {credentials}")
        return credentials

    def reset_credentials(self) -> None:
        """
        reset_credentials deletes any cached AWS credentials associated with the
        access token for this CredentialsManager instance.

        This will force new credentials to be fetched next time get_credentials()
        is called.
        """
        self._cache.delete(self._access_token)

    def _fetch_credentials(self) -> dict:
        """
        _fetch_credentials fetches temporary AWS credentials for the user associated
        with this CredentialsManager instance. It does the following:

        - Creates a boto3 client for the Cognito Identity service
        - Gets the identity provider from the id token payload
        - Calls GetId on the identity pool to get an identity id, providing the id token
          as a login
        - Calls GetCredentialsForIdentity to retrieve credentials using the identity id
          and id token
        - Extracts the credentials fields into a dict
        - Calculates the expiration time based on the Expiration field
        - Caches the credentials dict in the token cache using the access token as key
        - Returns the credentials dict

        The credentials will be valid until their expiration time. Subsequent calls
        to get_credentials will retrieve the cached credentials until they expire,
        at which point new credentials will be fetched.

        Returns:
            dict: The AWS credentials dict containing AccessKeyId, SecretKey,
                  and SessionToken

        """
        boto_client = boto3.client('cognito-identity')
        provider = self._id_token_payload['iss']
        provider = provider.replace('https://', '', 1)

        identity_pool_request_params = {
            'IdentityPoolId': self._identity_pool_id,
            'AccountId': settings.AWS_ACCOUNT_ID,
            'Logins': {
                provider: self._id_token
            }
        }
        logger.debug(f"ConnectionInjector middleware: get id params {identity_pool_request_params}")
        identity_pool_data = boto_client.get_id(**identity_pool_request_params)
        logger.debug(f"ConnectionInjector middleware: identity pool data {identity_pool_data}")
        identity_credentials_request_params = {
            'IdentityId': identity_pool_data.get('IdentityId'),
            'Logins': {
                provider: self._id_token
            }
        }
        logger.debug(f"ConnectionInjector middleware: get credentials params {identity_credentials_request_params}")
        user_credentials_data = boto_client.get_credentials_for_identity(**identity_credentials_request_params)
        credentials_dict = user_credentials_data.get('Credentials')
        logger.debug(f"ConnectionInjector middleware: credentials data {user_credentials_data}")

        delta = int((credentials_dict.get('Expiration') - datetime.datetime.now(tzlocal())).total_seconds())
        logger.debug(f"ConnectionInjector middleware: delta {delta}")

        credentials = {
            'aws_access_key_id': credentials_dict.get('AccessKeyId'),
            'aws_secret_access_key': credentials_dict.get('SecretKey'),
            'aws_session_token': credentials_dict.get('SessionToken'),
        }
        self._cache.set(self._access_token, credentials, timeout=delta - 10)
        return credentials
