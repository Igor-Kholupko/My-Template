from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin, GroupAdmin as _GroupAdmin
from django.contrib.auth.models import Group as _Group
from django.utils.translation import ugettext_lazy as _
from .models import User, Group


admin.site.unregister(_Group)


@admin.register(Group)
class GroupAdmin(_GroupAdmin):
    pass


@admin.register(User)
class UserAdmin(_UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email',)}),
        (_('Permissions'), {'fields': ('groups',)}),
    )
    list_display = ('username', 'email')
    list_filter = ('groups',)
    search_fields = ('username', 'email')
    ordering = ('-id',)
    filter_horizontal = ('groups',)
