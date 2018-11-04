from django.db import models
from django.utils.translation import ugettext_lazy as _
from custom_auth.models import User
from .validators import TemplateNameValidator


def _user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    if instance.user is None:
        return 'anonymous/{0}'.format(filename)
    else:
        return 'user_{0}/{1}'.format(instance.user.id, filename)


class Template(models.Model):
    """
    Template document and information represents by this model.

    Name and file are required. User owner sets automatic,
    but can be set manually by superuser at object creating through admin site.
    """
    name_validator = TemplateNameValidator()

    name = models.CharField(
        _('template name'),
        max_length=150,
        unique=False,
        help_text=_('Required. 150 characters or fewer. Letters, digits, whitespaces and @/./+/-/_ only.'),
        validators=[name_validator]
    )
    user = models.ForeignKey(
        User,
        models.SET_NULL,
        verbose_name=_('owner'),
        null=True,
        blank=True,
    )
    file = models.FileField(
        _('template file'),
        upload_to=_user_directory_path
    )
    email = models.EmailField(
        _('email address'),
        max_length=150,
        blank=False,
        help_text=_("Required if owner is anonymous user. Email allows to identify him in future.")
    )
    is_shared = models.BooleanField(
        _('is shared'),
        blank=False,
        default=False,
        help_text=_("This flag make template available to other user.")
    )
    description = models.TextField(
        _('description'),
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('template')
        verbose_name_plural = _('templates')

    def __str__(self):
        return self.name
