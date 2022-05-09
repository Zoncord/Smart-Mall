from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse

REDIRECT_FIELD_NAME = "user:profile"

def lessor_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url="user:profile"
):
    actual_decorator = user_passes_test(
        lambda u: u.is_lessor,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def tenant_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url="user:profile"
):
    actual_decorator = user_passes_test(
        lambda u: u.is_tenant,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
