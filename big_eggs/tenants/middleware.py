from django_scopes import scope, scopes_disabled


class SetTenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:
            if request.path.startswith("/admin"):
                # no scoping in admin
                with scopes_disabled():
                    response = self.get_response(request)
            else:
                with scope(tenant=request.user.tenant_id):
                    response = self.get_response(request)

        else:
            # logger.warning('no tenant')
            response = self.get_response(request)

        return response
