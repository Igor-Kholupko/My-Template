from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CustomAuthConfig(AppConfig):
    """
    Configuration class of 'custom_auth' application.
    """
    name = 'custom_auth'
    verbose_name = _("Authentication and Authorization")
