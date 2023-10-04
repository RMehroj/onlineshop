from django.contrib import admin

from . import models


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "owner",
        "name",
        "created",
        "is_active",
    ]


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "company",
        "social_media_id",
        "username",
        "full_name",
        "email",
        "phone",
        "role",
    ]

    ordering = [
        "-created",
    ]
