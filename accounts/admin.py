from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import User


class UserAdmin(BaseUserAdmin):

    list_display = ('id', 'phone', 'email', 'first_name', 'last_name', 'is_staff')
    list_display_links = ('id', 'phone')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'email', 'password')}
         ),
        ('Personal Info', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name')}
         ),
        ('Permissions', {
            'classes': ('wide',),
            'fields': ('is_staff',)}
         ),
    )
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('phone',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
