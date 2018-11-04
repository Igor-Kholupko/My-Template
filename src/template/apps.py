from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TemplateConfig(AppConfig):
    name = 'template'
    verbose_name = _("Templates")
