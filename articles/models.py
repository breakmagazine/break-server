from django.db import models

# Create your models here.
class Article(models.Model):
    image_url = models.URLField()