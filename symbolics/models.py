from django.db import models


class Symbolic(models.Model):
    symbolic_image = models.URLField(max_length=200)
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.symbolic_image