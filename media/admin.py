from django.contrib import admin

from media.models import Image


@admin.register(Image)
class ImageAmin(admin.ModelAdmin):
    pass