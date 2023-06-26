from django.db import models


class User(models.Model):
    id = models.SlugField(blank=False)
