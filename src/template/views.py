from django.contrib.admin.helpers import Fieldset
from templater.admin import site
from django.shortcuts import HttpResponseRedirect, render
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView, View

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
    template_name = 'site/template/template_creation_form.html'
    success_url = reverse_lazy('home')
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
            model_admin=site.get_model_admin(Template)
        )
        return context


class TemplateList(ListView):
    """
    Generic list view to show all shared templates in grid view.
    """
    model = Template
    paginate_by = 8
    template_name = 'site/template/template_list_form.html'
    extra_context = {
        'search_var': 'q'
    }
    ordering = '-id'

    def dispatch(self, request, *args, **kwargs):
        user = self.kwargs.get('user')
        if user is not None:
            if request.user.is_anonymous or request.user.id != user:
                return HttpResponseRedirect(reverse_lazy('home'))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.queryset = super().get_queryset()
        user = self.kwargs.get('user')
        search_query = self.request.GET.get('q')
        if user is not None:
            self.queryset = self.queryset.filter(user_id__exact=user)
        else:
            self.queryset = self.queryset.filter(is_shared__exact=True)
        if search_query is not None:
            self.queryset = self.queryset.filter(name__icontains=search_query)
        return self.queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        extra_content = {}
        search_query = self.request.GET.get('q')
        if search_query is not None:
            extra_content.update({'search_query': search_query})
        context.update(extra_content)
        return context


class TemplateDetail(DetailView):
    """
    Show details about selected template.
    """
    model = Template
    template_name = 'site/template/template_detail_form.html'

    def __init__(self, **kwargs):
        self.object = None
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        is_owner = self.object.user_id and self.object.user_id == request.user.id
        if not self.object.is_shared and not is_owner:
            return HttpResponseRedirect(reverse_lazy('home'))
        context = self.get_context_data(object=self.object, is_owner=is_owner)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if '_share' in request.POST:
            self.object.is_shared = True
        elif '_hide' in request.POST:
            self.object.is_shared = False
        elif '_edit' in request.POST and 'description' in request.POST:
            self.object.description = request.POST.get('description')
        if 'file' in request.FILES:
            self.object.helper.is_reuploaded = True
            self.object.file = request.FILES.get('file')
        self.object.save()
        return HttpResponseRedirect(request.path_info)


class TemplateDelete(DeleteView):
    """
    Delete confirmation view.
    """
    model = Template
    template_name = 'site/template/template_delete_confirmation_form.html'

    def __init__(self, **kwargs):
        self.object = None
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if (request.user.is_anonymous or self.object.user_id != request.user.id) and not request.user.is_staff:
            return HttpResponseRedirect(reverse_lazy('home'))
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy('template_list', kwargs={'user': self.request.user.id})


class TemplatePreview(View):
    """
    Generic preview page for template (available only for widescreen). Uses <iframe> tag.
    """
    model = Template
    template_name = 'site/template/template_preview_form.html'

    def __init__(self, **kwargs):
        self.object = None
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.model.objects.get(pk=kwargs.get('pk'))
        if not self.object.is_shared and self.object.user_id != request.user.id:
            return HttpResponseRedirect(reverse_lazy('home'))
        context = {'file': self.object.file.name}
        return render(request, self.template_name, context, using='MEDIA_ENGINE')
