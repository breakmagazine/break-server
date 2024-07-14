from django.db import models
from django.conf import settings


class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    thumbnail_image = models.URLField()
    category = models.CharField(max_length=50)
    sub_category = models.CharField(max_length=50, null=True, blank=True)  # ㅊㅁㅅ
    magazine_number = models.IntegerField()
    collaborators = models.JSONField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    look_info = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
