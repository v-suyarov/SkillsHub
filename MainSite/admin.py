from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm
from datetime import date



class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

class StudentAdmin(admin.ModelAdmin):
    readonly_fields = ('age',)

    def save_model(self, request, obj, form, change):
        # Вызовите родительский метод, чтобы сохранить объект модели
        super().save_model(request, obj, form, change)
        obj.age = date.today().year - obj.date_of_birth.year - (
                    (date.today().month, date.today().day) < (obj.date_of_birth.month, obj.date_of_birth.day))
        obj.save()

admin.site.register(Student, StudentAdmin)
admin.site.register(Skill)
admin.site.register(Group)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)