from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Team, TeamMember


class UserAdmin(BaseUserAdmin):
    list_display = (
        "email",
        "name",
        "active",
        "admin",
    )
    list_filter = (
        "admin",
        "active",
    )
    filter_horizontal = ()
    ordering = ("email",)
    search_fields = ('email', "name",)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('staff', 'admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Team)
admin.site.register(TeamMember)
