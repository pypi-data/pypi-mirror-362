from rest_framework import status
from django.http import JsonResponse
from django.contrib.auth.models import AnonymousUser

from django_rds_iam_auth.models import Tenant


class CheckTenantStatusMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
                not isinstance(request.user, AnonymousUser)
                and not request.user.is_superuser
                and not Tenant.objects.get(id=request.user.origin_tenant_id).is_active
        ):
            response = JsonResponse(
                data={'message': 'Your organization account is no longer available, please contact your administrator'},
                status=status.HTTP_403_FORBIDDEN,
            )
        else:
            response = self.get_response(request)

        return response
