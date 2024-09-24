""" Project interface settings """

from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.models import Group
from .models import CustomUser, Task

admin.site.unregister(Group)


@admin.register(CustomUser)
class UsersAdmin(auth_admin.UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active']
    search_fields = []
    readonly_fields = ('last_login', 'date_joined',)
    list_filter = []

    fieldsets = (('Personal info', {'fields': ('username', 'first_name', 'last_name', 'email', 'password')}),
                 ('Permissions', {'fields': ('is_active',)}),
                 ('Important dates', {'fields': ('date_joined', 'last_login')}))

    def get_queryset(self, request):
        queryset = CustomUser.objects.filter(id=request.user.id)
        return queryset


@admin.register(Task)
class TasksAdmin(admin.ModelAdmin):
    list_display = ('task', 'category', 'creation_datetime', 'deadline', 'prioritize', 'status', )
    exclude = ['creation_datetime', 'user']
    ordering = ['-status', 'prioritize', 'creation_datetime']
    list_filter = ['status', 'prioritize']

    def get_queryset(self, request):
        queryset = Task.objects.filter(user_id=request.user)
        return queryset

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)
