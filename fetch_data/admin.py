from django.contrib import admin
from fetch_data.models import Piscine, User, Project, CursusProject, Cursus, ClusterLocation, UsefulLink
from fetch_data.models import Key

# Register your models here.

class KeyAdmin(admin.ModelAdmin):
    list_display = ['name', 'uid', 'token', 'valid_until', 'expire_date']
    search_fields = ['name', 'uid']


class PiscineAdmin(admin.ModelAdmin):
    list_display = ['month', 'year', 'user_count']
    search_fields = ['month', 'year']


class UserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'login', 'evaluation_points', 'updated_at', 'wallet', 'display_favorite_users']
    search_fields = ['user_id', 'login']
    list_filter = ['piscine', 'active']

    def display_favorite_users(self, obj):
        return ", ".join([str(user.login) for user in obj.favorite_users.all()])

    display_favorite_users.short_description = 'Favorite Users'


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'final_mark', 'marked_at', 'user', 'cursus_id']
    search_fields = ['name', 'status', 'final_mark', 'user__login']
    list_filter = ['cursus_id']


class CursusProjectAdmin(admin.ModelAdmin):
    list_display = ['project_id', 'name', 'difficulty', 'estimate_time', 'is_subscriptable']
    search_fields = ['name', 'difficulty', 'estimate_time']


class CursusAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'begin_at', 'blackholed_at', 'cursus_id', 'user']
    search_fields = ['name', 'level', 'cursus_id', 'user__login']


class ClusterLocationAdmin(admin.ModelAdmin):
    list_display = ['host', 'begin_at', 'user']
    search_fields = ['host', 'user__login']


class UsefulLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'url', 'creator', 'link_creator')


admin.site.register(Key, KeyAdmin)

admin.site.register(Piscine, PiscineAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Cursus, CursusAdmin)

admin.site.register(CursusProject, CursusProjectAdmin)
admin.site.register(ClusterLocation, ClusterLocationAdmin)

admin.site.register(UsefulLink, UsefulLinkAdmin)


