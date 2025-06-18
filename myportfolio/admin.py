from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "featured")
    fields = (
        "title",
        "subtitle",
        "slug",
        "description",
        "media",
        "featured",
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
