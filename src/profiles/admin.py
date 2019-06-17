from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('user', )
    fields = ('user', 'activation_key', 'activated')
    list_display = ['user', 'activated']
    list_filter = ['activated']
    search_fields = ['user']


admin.site.register(Profile, ProfileAdmin)
