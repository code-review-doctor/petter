from django.contrib import admin
# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from users.forms import CustomUserChangeForm
from users.forms import CustomUserCreationForm

CustomUser = get_user_model()


class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'age', 'is_active', ]


admin.site.register(CustomUser, CustomUserAdmin)

admin.site.unregister(Group)
