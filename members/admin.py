from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import Profile, GroupRole

User = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "profile"
    fk_name = "user"


# Try to extend the default user admin to include the Profile inline.
try:
    # unregister existing registration and re-register with inline
    admin.site.unregister(User)
except Exception:
    # If it wasn't registered or unregister fails, we'll attempt to register later
    pass


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    inlines = (ProfileInline,)

    def get_inline_instances(self, request, obj=None):
        # Avoid errors when dealing with custom user models that don't have a profile yet
        inline_instances = []
        for inline_class in self.inlines:
            inline = inline_class(self.model, self.admin_site)
            inline_instances.append(inline)
        return inline_instances


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "role", "phone", "company")
    search_fields = ("user__username", "user__email", "company", "phone")
    list_filter = ("role",)


@admin.register(GroupRole)
class GroupRoleAdmin(admin.ModelAdmin):
    list_display = ("group", "role")
    list_filter = ("role", "group")