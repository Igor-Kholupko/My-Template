from django.contrib.auth.forms import UserCreationForm

from custom_auth.models import User


class UserRegistrationForm(UserCreationForm):
    """
    User registration form class. Extends default UserCreationForm class.

    Email was added to required fields.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'class': 'vTextField'})
        if self._meta.model.EMAIL_FIELD in self.fields:
            self.fields[self._meta.model.EMAIL_FIELD].widget.attrs.update({'class': 'vTextField'})

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')
