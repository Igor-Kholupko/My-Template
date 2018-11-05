from django.contrib.admin.helpers import Fieldset
from django.contrib.auth.views import LoginView as _LoginView
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import CreateView

from custom_auth.models import User
from custom_auth.forms import UserRegistrationForm


class LoginView(_LoginView):
    """
    Extended LoginView class with decorator to redirect authenticated users.
    """
    @method_decorator(user_passes_test(lambda u: not u.is_authenticated, login_url='/'))
    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class RegistrationView(CreateView):
    """
    Generic view class for creating new user through registration form.
    """
    model = User
    form_class = UserRegistrationForm
    template_name = 'registration/registration_form.html'
    success_url = '/accounts/login'
    extra_context = {
        'title': _("New user registration")
    }

    @method_decorator(user_passes_test(lambda u: not u.is_authenticated, login_url='/'))
    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fieldset'] = Fieldset(
            form=context['form'],
            name=None,
            readonly_fields=(),
            classes=('wide',),
            fields=self.form_class.Meta.fields
        )
        return context
