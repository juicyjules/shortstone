from django.db import models

# Create your models here.
class Url(models.Model):
    slug = models.CharField(max_length=20)
    url = models.CharField(max_length=500)
    def __str__(self):
        return self.slug+"://"+self.url