import hashlib
from django.db import models


class Image(models.Model):
    title = models.CharField(max_length=128, null=True, blank=True)
    image = models.ImageField(width_field="width", height_field="height", upload_to="images/")

    width = models.IntegerField(editable=False)
    height = models.IntegerField(editable=False)
    file_hash = models.CharField(max_length=40, db_index=True, editable=False)
    file_size = models.PositiveIntegerField(null=True, editable=False)

    def __str__(self):
        return f"{self.title} image"

    def save(self, *args, **kwargs):
        if not self.image.file.closed:

            self.file_size = self.image.size

            hasher = hashlib.sha1()
            for chunk in self.image.file.chunks():
                hasher.update(chunk)
            self.file_hash = hasher.hexdigest()

        super().save(*args, **kwargs)
