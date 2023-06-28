from datetime import datetime
from enum import Enum

from django.db import models

from management.models import User


class NewsSource(str, Enum):
    mind = "MIND"


class NewsArticle(models.Model):
    id = models.SlugField(primary_key=True, blank=False)
    source = models.CharField(
        choices=[(NewsSource.mind, "Microsoft News Dataset")],
        default=NewsSource.mind,
        blank=False,
    )
    category = models.CharField(max_length=20)
    subcategory = models.CharField(max_length=40)
    title = models.TextField(blank=False)
    abstract = models.TextField()
    url = models.URLField(blank=False)
    publishing_date = models.DateTimeField(default=datetime.now, blank=False)


class NewsImpression(models.Model):
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    article = models.ForeignKey(NewsArticle, blank=False, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.now, blank=False)
    session = models.SlugField(blank=False, default="missing_session")
