from django.db import models
from slugify import slugify


class ToolTask(models.Model):
    name = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(ToolTask, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
