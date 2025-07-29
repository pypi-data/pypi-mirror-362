from django.conf import settings
from django_rds_iam_auth.middleware.jwt_exposer import local


class GenericRLSSecuredRouter:
    """
    DB Router to control which type of connection pool will be used, default / RLS secured
    The RLS secured pool stores connections in REDIS cache (the rls_iam_auth package generates the cache for any new instance using
    cognito service, the TTL is taken from cognito token expiration dateTime

    Notice this router is for operational work only and will not (and should not be) used for running migrations
    the responsibility for migrations resides with the host app.
    """
    excluded_apps = settings.EXCLUDE_APP_FROM_SECURE_RLS

    @staticmethod
    def has_method(o, name):
        return callable(getattr(o, name, None))

    def db_for_read(self, model, **hints):
        """
        If Model is not in excluded app - use RLS Secure Connection.
        """
        if model._meta.app_label not in self.excluded_apps and hasattr(local, 'user_id'):
            return local.user_id
        return None

    def db_for_write(self, model, **hints):
        """
        If Model is not in excluded app - use RLS Secure Connection.
        """
        if model._meta.app_label not in self.excluded_apps and hasattr(local, 'user_id'):
            return local.user_id
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Responsibility of host app.
        """
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Responsibility of host app.
        """
        return None
