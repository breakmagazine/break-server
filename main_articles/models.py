from django.db import models


class MainArticle(models.Model):
    main_article1 = models.URLField(max_length=200)
    main_article2 = models.URLField(max_length=200)
    main_article1_redirect_url = models.URLField(max_length=200)
    main_article2_redirect_url = models.URLField(max_length=200)

    def __str__(self):
        return f"MainArticle {self.id}"