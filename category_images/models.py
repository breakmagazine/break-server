from django.db import models


class CategoryImage(models.Model):
    CATEGORY_CHOICES = [
        ('ABOUT', 'About'),
        ('FASHION', 'Fashion'),
        ('FEATURE', 'Feature'),
        ('PHOTOGRAPHY', 'Photography'),
        ('FILM', 'Film'),
        ('ART', 'Art'),
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    image_url = models.URLField(max_length=200)

    def __str__(self):
        return self.category