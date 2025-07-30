from ..context.context_vars import tenant_context


# def get_auth_user():
#     return auth_user_context.get()


def get_tenant_code():
    return tenant_context.get()
