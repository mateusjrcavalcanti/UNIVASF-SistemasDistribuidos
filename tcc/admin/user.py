import types
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.forms import AdminAuthenticationForm
from tcc.models import User


def has_permission(self, request):
    return request.user.is_active and (
        request.user.is_staff
        or request.user.groups.filter(name="Discentes").exists()
        or request.user.groups.filter(name="Docentes").exists()
    )


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('titulo', 'first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        })
    )


class GrpAdminAuthenticationForm(AdminAuthenticationForm):
    def confirm_login_allowed(self, user):
        if user.groups.filter(name="Discentes").exists() or user.groups.filter(name="Docentes").exists():
            user.is_staff = True
        super().confirm_login_allowed(user)


admin.site.login_form = GrpAdminAuthenticationForm
admin.site.has_permission = types.MethodType(has_permission, admin.site)
