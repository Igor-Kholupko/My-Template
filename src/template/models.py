from os.path import relpath
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from custom_auth.models import User
from template.validators import TemplateNameValidator
from template.utils import create_thumbnail, make_thumbnail_save_path
from template.validators import HtmlExtensionValidator


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
        upload_to=_user_directory_path,
        validators=[HtmlExtensionValidator()]
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

    def delete(self, using=None, keep_parents=False):
        try:
            self.file.storage.delete(self.helper.thumbnail)
        except TemplateHelper.DoesNotExist:
            self.file.storage.delete(make_thumbnail_save_path(self.file.path))
        self.file.delete()
        return super().delete(using, keep_parents)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        try:
            if self.helper.is_reuploaded:
                self.file.storage.delete(self.helper.thumbnail)
                self.file.storage.delete(self.helper.file)
                self.helper.thumbnail = create_thumbnail(self.file.path)
                self.helper.file = self.file.path
                self.helper.is_reuploaded = False
                self.helper.save()
        except TemplateHelper.DoesNotExist:
            TemplateHelper.objects.create(
                template=self,
                thumbnail=create_thumbnail(self.file.path),
                file=self.file.path,
                is_reuploaded=False
            )


class TemplateHelper(models.Model):
    template = models.OneToOneField(
        Template,
        on_delete=models.CASCADE,
        related_name='helper',
        primary_key=True
    )
    thumbnail = models.CharField(
        max_length=260,
        blank=True,
        null=True,
        default=None
    )
    file = models.CharField(
        max_length=260,
        blank=True,
        null=True,
        default=None
    )
    is_reuploaded = models.BooleanField(
        blank=False,
        default=False
    )

    @property
    def thumbnail_media(self):
        return relpath(self.thumbnail, settings.MEDIA_ROOT)

    class Meta:
        verbose_name = _('template meta')
        verbose_name_plural = _('templates meta')

    def __str__(self):
        return "'{}'-{}".format(
            self.template.name,
            _('meta')
        )
