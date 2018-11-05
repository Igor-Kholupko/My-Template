from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TemplateConfig(AppConfig):
    """
    Configuration class of 'template' application.
    """
    name = 'template'
    verbose_name = _("Templates")
