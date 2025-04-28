from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


# Register the custom user model with custom display fields
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['id', 'username', 'email', 'is_staff', 'is_active', 'last_login']
    search_fields = ['username', 'email']
    ordering = ['id']


admin.site.register(User, CustomUserAdmin)
