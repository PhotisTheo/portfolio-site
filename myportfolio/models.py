from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from storages.backends.s3boto3 import S3Boto3Storage  # since you're using S3


class Project(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()

    # 👇 Change this field
    media = models.FileField(
        upload_to="projects/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "gif", "mp4"]
            )
        ],
        storage=S3Boto3Storage(),
        blank=True,
        null=True,  # 👈 This is the fix
    )

    body = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True)
    client = models.CharField(max_length=100, blank=True)
    start_date = models.DateField(blank=True, null=True)
    designer = models.CharField(max_length=100, blank=True)
    featured = models.BooleanField(default=False)

    featured_media = models.FileField(
        upload_to="projects/featured/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "gif", "mp4"]
            )
        ],
        storage=S3Boto3Storage(),
    )

    date_created = models.DateTimeField(auto_now_add=True)

    # (Optional: update gallery images if needed)
    gallery_image_1 = models.ImageField(
        upload_to="projects/gallery/", blank=True, null=True, storage=S3Boto3Storage()
    )
    gallery_image_2 = models.ImageField(
        upload_to="projects/gallery/", blank=True, null=True, storage=S3Boto3Storage()
    )
    gallery_image_3 = models.ImageField(
        upload_to="projects/gallery/", blank=True, null=True, storage=S3Boto3Storage()
    )

    extra_title = models.CharField(max_length=255, blank=True)
    extra_paragraph = models.TextField(blank=True)

    accordion_1_title = models.CharField(max_length=255, blank=True)
    accordion_1_body = models.TextField(blank=True)
    accordion_2_title = models.CharField(max_length=255, blank=True)
    accordion_2_body = models.TextField(blank=True)
    accordion_3_title = models.CharField(max_length=255, blank=True)
    accordion_3_body = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"slug": self.slug})
