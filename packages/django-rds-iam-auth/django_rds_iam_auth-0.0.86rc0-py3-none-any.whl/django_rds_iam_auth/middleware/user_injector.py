from django_rds_iam_auth.models import User
from django_rds_iam_auth.middleware.jwt_exposer import local


class UserInjector:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(local, 'user_id') and local.user_id is not None:
            request.user = User.objects.get(id=local.user_id)

        response = self.get_response(request)

        return response
