from django.core import validators
from django.core.exceptions import ValidationError
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


@deconstructible
class HtmlExtensionValidator(validators.FileExtensionValidator):
    html_heading = '<!DOCTYPE html>'.lower()
    html_extension = 'html'
    invalid_content_message = _(
        "File content should be HTML template document."
    )
    invalid_content_code = 'invalid_content'

    def __init__(self, allowed_extensions=None, message=None, code=None):
        super().__init__(allowed_extensions, message, code)
        self.allowed_extensions = (self.html_extension,)

    def __call__(self, value):
        super().__call__(value)
        heading = value.file.readline()
        while heading.decode().strip().lower().__len__() == 0:
            if heading.__len__() == 0:
                break
            heading = value.file.readline()
        if heading.decode().strip().lower() != self.html_heading:
            raise ValidationError(
                self.invalid_content_message,
                code=self.invalid_content_code,
            )
