from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class TemplateNameValidator(validators.RegexValidator):
    """
    Class for validating template name field.
    """
    regex = r'^[ \w.@+-]+$'
    message = _(
        'Enter a valid template name. This value may contain only letters, '
        'numbers, whitespaces, and @/./+/-/_ characters.'
    )
    flags = 0
