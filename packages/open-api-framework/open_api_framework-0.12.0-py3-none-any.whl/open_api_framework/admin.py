from django.contrib import admin

from sessionprofile.models import SessionProfile

from open_api_framework.utils import get_session_store


@admin.register(SessionProfile)
class SessionProfileAdmin(admin.ModelAdmin):
    list_display = ["session_key", "user", "exists"]

    @property
    def SessionStore(self):
        return get_session_store()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user=request.user)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    @admin.display(boolean=True)
    def exists(self, obj):
        return self.SessionStore().exists(obj.session_key)

    def delete_model(self, request, obj):
        self.SessionStore(obj.session_key).flush()
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for session_profile in queryset.iterator():
            self.SessionStore(session_profile.session_key).flush()

        super().delete_queryset(request, queryset)
