from django.db import models

class MainBanner(models.Model):
    banner1 = models.URLField(max_length=200)
    banner2 = models.URLField(max_length=200)
    banner3 = models.URLField(max_length=200)
    banner4 = models.URLField(max_length=200)
    banner5 = models.URLField(max_length=200)

class CentralBanner(models.Model):
    banner = models.URLField(max_length=200)