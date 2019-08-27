from django.db import models
from slugify import slugify


class Tool(models.Model):
    name = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super(Tool, self).save(*args, **kwargs)
