from django import forms
from django.utils.translation import ugettext_lazy as _

from template.models import Template


class UserModelChoiceField(forms.ModelChoiceField):
    """
    Class of user choose field, that redefines empty label value.
    """
    def __new__(cls, *args, **kwargs):
        instance = forms.ModelChoiceField(*args, **kwargs)
        instance.empty_label = _("Anonymous user")
        return instance


class TemplateAdminForm(forms.ModelForm):
    """
    Class of create and change form for admin site.

    Control queries for valid user and email field matching.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            try:
                self.fields['user'].widget.attrs['readonly'] = True
            except KeyError:
                pass

    def _clean_fields(self):
        super()._clean_fields()
        email_error = self._errors.get('email')
        if email_error is not None and (email_error.data.__len__() == 1 and email_error.data[0].code == 'required'):
            if self.cleaned_data.get('user') is not None:
                self._errors.pop('email')

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('user') is not None:
            cleaned_data.update({'email': cleaned_data.get('user').email})
        if self.instance.pk is not None and 'file' in self.changed_data:
            self.instance.helper.is_reuploaded = True
            self.instance.helper.save()
        return cleaned_data

    def clean_user(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            return instance.user
        else:
            return self.cleaned_data['user']

    class Meta:
        model = Template
        fields = '__all__'
        field_classes = {
            'user': UserModelChoiceField
        }


class TemplateCreateForm(TemplateAdminForm):
    """
    Class of form for template uploading.

    Same as TemplateAdminForm but with another fieldset.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'name' in self.fields:
            self.fields['name'].widget.attrs.update({'class': 'vTextField'})
        if 'email' in self.fields:
            self.fields['email'].widget.attrs.update({'class': 'vTextField'})

    class Meta:
        model = Template
        fields = ('name', 'email', 'file', 'is_shared', 'description', 'user')
