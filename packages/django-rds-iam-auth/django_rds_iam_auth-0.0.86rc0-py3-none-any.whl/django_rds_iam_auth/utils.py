import datetime
import dns.resolver
import dns.rdatatype
from dns.exception import DNSException

import boto3
from django.db import connections
from django.utils.connection import ConnectionProxy


def is_useful(alias: str, raise_exception: bool = False) -> bool:
    try:
        ConnectionProxy(connections, alias).cursor()
        return True
    except Exception as e:
        if raise_exception:
            raise e
        return False


def create_connection(default_connection: dict, alias: str, credentials: dict) -> dict:
    boto3_session = boto3.session.Session(**credentials)
    rds_client = boto3_session.client("rds", **credentials)
    default_connection['id'] = alias
    default_connection['USER'] = alias
    default_connection['ENGINE'] = 'django_rds_iam_auth.aws.postgresql'
    default_connection['CONN_MAX_AGE'] = 2 * 60  # seconds
    default_connection['PASSWORD'] = rds_client.generate_db_auth_token(
        DBHostname=default_connection['HOST'],
        Port=default_connection.get("port", 5432),
        DBUsername=alias,
    )
    return default_connection


def resolve_cname(hostname):
    """Resolve a CNAME record to the original hostname.

    This is required for AWS where the hostname of the RDS instance is part of
    the signing request.

    """
    try:
        answers = dns.resolver.query(hostname, "CNAME")
        for answer in answers:
            if answer.rdtype == dns.rdatatype.CNAME:
                return answer.to_text().strip('.')
    except DNSException:
        return hostname


def set_cookie(response, domain, key, value, days_expire=7, secure=None):
  if days_expire is None:
    max_age = 365 * 24 * 60 * 60  #one year
  else:
    max_age = days_expire * 24 * 60 * 60
  expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
  response.set_cookie(key, value, max_age=max_age, expires=expires, domain=domain, secure=secure or None)

