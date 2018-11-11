from templater import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin, GroupAdmin
from django.utils.translation import ugettext_lazy as _

from custom_auth.models import User, Group


# Registration of custom Group model instead of default.
admin.site.register(Group, GroupAdmin)


@admin.register(User)
class UserAdmin(_UserAdmin):
    """
    Class for admin generic views of User model.

    Includes default admin options.
    """
    add_form_template = 'admin/custom_auth/user/add_form.html'
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email',)}),
        (_('Permissions'), {'fields': ('groups',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email')
    list_filter = ('groups',)
    search_fields = ('username', 'email')
    ordering = ('-id',)
    filter_horizontal = ('groups',)
