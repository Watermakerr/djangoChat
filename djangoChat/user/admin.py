from django.contrib.auth.admin import UserAdmin
from .models import User, FriendRequest
from django.contrib import admin

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'gender', 'birth_date', 'phoneNumber', 'display_friends']
    fieldsets = (
        (None, {'fields': ('username', 'first_name', 'last_name', 'email', 'password', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions', 'avatar', 'gender', 'birth_date', 'phoneNumber', 'friends')}),
    )
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['username']

    def display_friends(self, obj):
        return ", ".join([friend.username for friend in obj.friends.all()])
    display_friends.short_description = 'Friends'

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(CustomUserAdmin, self).get_fieldsets(request, obj)

admin.site.register(User, CustomUserAdmin)
admin.site.register(FriendRequest)