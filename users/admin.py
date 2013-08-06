""" Admin page configuration for the users app """
from django.contrib import admin

from users.models import User
from users.forms import UserCreationForm
from users.forms import UserChangeForm

from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _


class UserAdmin(DjangoUserAdmin):
    """ Configuration for the User admin page"""
    add_form_template = 'admin/users/user/add_form.html'

    add_form = UserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff',
                    'change_password_link')
    form = UserChangeForm
    fieldsets = (
        (None, {'fields': ('email',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1',
                       'password2')}
         ),
    )
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)

    def change_password_link(self, obj):
        return u"<a href=\"%d/password/\">%s</a>" % (obj.id,
                                                     _("change password"))
    change_password_link.allow_tags = True
    change_password_link.short_description = _("change password")

admin.site.register(User, UserAdmin)
