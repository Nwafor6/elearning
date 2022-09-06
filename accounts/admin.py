from django.contrib import admin

from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from . import models 
from . import forms 
from commonapps.models import Cohort
# Register your models here.

admin.site.register(Cohort)
@admin.register(models.CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = forms.CustomUserCreationForm
    form = forms.CustomUserChangeForm
    model = models.CustomUser

    ordering = ["email"]
    list_display = ["email","first_name","last_name",'cohort',"is_staff", "is_active","is_superuser",]
    search_fields = ["email"]
    
    fieldsets = (
        (None, {
            "fields": (
                'email', 'password'
            ),
        }),
        ('Details', {
            "fields": (
                'first_name', 'last_name', 'cohort','slug','is_admin', 'is_instructor', 'is_learner'
            ),
        }),
        ('Permissions', {
            "fields": (
                'is_staff', 'is_active'
            ),
        }),
    )
    add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('email', 'first_name', 'last_name', 'password1', 'password2','cohort','is_admin', 'is_instructor', 'is_learner'),
    }),
)


