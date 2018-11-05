from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from template.models import Template
from template.forms import TemplateAdminForm


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    """
    Class for admin generic views of Template model.

    Include user-defined options and overrides some basic methods
    besides of using default options.
    """
    add_form_template = 'admin/template/add_form.html'
    fieldsets = (
        (_("Template information"), {
            'fields': ('name', 'user', 'email', 'is_shared', 'description'),
        }),
        (_("Media files"), {
            'fields': ('file',),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'file', 'user', 'email'),
        }),
    )
    form = TemplateAdminForm
    add_readonly_fields = ()
    readonly_fields = ('user', 'email')
    list_display = ('name', 'user_field', 'is_shared')
    search_fields = ('name',)
    ordering = ('-id',)

    def user_field(self, obj):
        return obj.user
    user_field.short_description = _("owner")
    user_field.empty_value_display = _("Anonymous user")
    user_field.admin_order_field = 'user'

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return self.add_readonly_fields
        return super().get_readonly_fields(request, obj)

    def get_empty_value_display(self):
        return mark_safe(_("Anonymous user"))
