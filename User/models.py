from ast import Delete
from contextlib import nullcontext
from email.policy import default
from enum import unique
from pickle import TRUE
from random import choices
from re import A
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser
from pkg_resources import require
from Gym.models import Gyms

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

UserType = (
        ("1", "Administrator"),
        ("2", "Trainer"),
        ("3", "Member"),
    )

Gender = (
        ("1", "Masculino"),
        ("2", "Femenino"),
        ("3", "Otro"),
    )

class UsersTypes(models.Model):
    description = models.CharField(max_length = 15, null = False, unique = True)

    def __str__(self):
        return self.description

class Users(AbstractUser):
    rut         = models.CharField(max_length = 12, null = False, unique = True)
    gender      = models.CharField(choices = Gender, max_length = 10, null = False)
    birthday    = models.DateField(null = True)

class Administrators(models.Model):
    gyms        = models.ManyToManyField(Gyms)
    user        = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key = True)

class Trainers(models.Model):
    gyms        = models.ManyToManyField(Gyms)
    user        = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key = True)

class Members(models.Model):
    gyms        = models.ManyToManyField(Gyms)
    user        = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key = True)