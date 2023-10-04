from django.contrib import admin

from . import models

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "name",
        "description",
        "parent",
        "slug",
        "image",
    ]


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "name",
        "company",
        "website",
        "slug",
        "price",
    ]
    filter_horizontal = [
        "categories",
    ]
    ordering = [
        "-created",
    ]

