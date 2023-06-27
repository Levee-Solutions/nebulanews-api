from django.db import models


class User(models.Model):
    id = models.SlugField(primary_key=True, blank=False)
