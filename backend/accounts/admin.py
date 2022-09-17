from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "email",
        "username",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "username",
                    "password",
                    "avatar",
                )
            }
        ),
        (
            "Profile",
            {
                "fields": (
                    "followers",
                    "pending_requests",
                    "blocked_users",
                )
            }
        ),
    )
