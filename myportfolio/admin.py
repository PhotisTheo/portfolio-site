from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "featured", "popup_featured", "category")
    list_filter = ("featured", "popup_featured", "category")
    fields = (
        "title",
        "subtitle",
        "slug",
        "description",
        "media",
        "featured",
        "popup_featured",
        "popup_blurb",
        "featured_media",
        "body",
        "category",
        "client",
        "start_date",
        "designer",
        "gallery_image_1",
        "gallery_image_2",
        "gallery_image_3",
        "extra_title",
        "extra_paragraph",
        "accordion_1_title",
        "accordion_1_body",
        "accordion_2_title",
        "accordion_2_body",
        "accordion_3_title",
        "accordion_3_body",
    )
