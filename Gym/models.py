from django.db import models

# Create your models here.

class Gyms(models.Model):
    name        = models.CharField(max_length = 100, null = False)
    direction   = models.CharField(max_length = 100, null = False)

    def __str__(self):
        return self.name