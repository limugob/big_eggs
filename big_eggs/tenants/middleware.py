from django_scopes import scope


class SetTenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:
            tenant = request.user.tenant_set.first()
            with scope(tenant=tenant.id):
                response = self.get_response(request)

        else:
            # logger.warning('no tenant')
            response = self.get_response(request)

        return response
