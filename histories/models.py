from django.db import models


class History(models.Model):
    image_url = models.URLField(max_length=200)
    published_at = models.DateField()
    publication_number = models.IntegerField()
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} ({self.published_at})"