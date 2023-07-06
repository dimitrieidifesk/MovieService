import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class MovieTypes(models.TextChoices):
    movie = "movie"
    serial = "serial"


class Movies(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=120, unique=True)
    type = models.CharField(max_length=50, choices=MovieTypes.choices)
    rating = models.FloatField()
    description = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "movies"
        verbose_name = _("Movie")
        verbose_name_plural = _("Movies")
