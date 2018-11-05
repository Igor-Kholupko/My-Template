from django.contrib.admin.helpers import Fieldset
from django.contrib.admin import site
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView

from template.models import Template
from template.forms import TemplateCreateForm


class TemplateCreate(CreateView):
    """
    Class of generic view for uploading/sharing page.

    Handle post request and pass user owner of request to creation form.
    Provides all required data to render fieldsets.
    """
    model = Template
    form_class = TemplateCreateForm
    template_name = 'admin/template/template_creation_form.html'
    success_url = '/templates/create/'
    extra_context = {
        'title': _("New template uploading"),
        'title_anon': _("Template sharing"),
        'has_file_field': True
    }

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: passing user id or is_shared inside POST request.
        """
        request.POST._mutable = True
        if request.user.is_anonymous:
            request.POST.update({'is_shared': 'on'})
        request.POST.update({'user': str(request.user.id) if request.user.is_authenticated else ''})
        request.POST._mutable = False
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = [
            field
            for field in self.form_class.Meta.fields
            if field != 'user'
        ]
        readonly_fields = ()
        if context.get('view').request.user.is_anonymous:
            readonly_fields = ('is_shared',)
            context.get('form').instance.is_shared = True
        else:
            fields.remove('email')
        context['fieldset'] = Fieldset(
            form=context.get('form'),
            name=None,
            readonly_fields=readonly_fields,
            classes=('wide',),
            fields=fields,
            model_admin=site._registry.get(Template)
        )
        return context


def home_page(request):
    return render(request, 'site/base.html')
