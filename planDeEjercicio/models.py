from email.policy import default
#from fcntl import F_SEAL_SEAL
from pydoc import describe
from random import choices
from tkinter.tix import Tree
from unittest.util import _MAX_LENGTH
from django.db import models
from django.forms import IntegerField
from django.contrib import admin

from User.models import *

# Create your models here.
DAYS = (
        ("1", "Lunes"),
        ("2", "Martes"),
        ("3", "Miercoles"),
        ("4", "Jueves"),
        ("5", "Viernes"),
        ("6", "Sabado"),
        ("7", "Domingo")
    )

class ExercisePlans(models.Model):
    id      = models.AutoField(primary_key = True)
    date    = models.DateField(auto_now_add = True)
    member  = models.ForeignKey(Members, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.id) + "    |   " + str(self.date)

class Exercises(models.Model):
    id                  = models.AutoField(primary_key = True)
    nombre              = models.CharField(null = False, max_length = 50, blank = True)
    numeroMaquina       = models.IntegerField(null = True)
    descripcion         = models.CharField(null = False, max_length = 250)
    series              = models.IntegerField(null = False)
    repeticiones        = models.IntegerField(null = False)
    carga               = models.IntegerField(null = False)
    descanso_minutos    = models.IntegerField(null = False)
    video               = models.URLField(null = True)

class Routines(models.Model):
    id              = models.AutoField(primary_key = True)
    description     = models.CharField(null = False, max_length = 50)
    day             = models.CharField(choices = DAYS, max_length = 9)
    image           = models.URLField(null=True)
    ExercisePlan    = models.ForeignKey(ExercisePlans, on_delete = models.CASCADE)
    Exercise        = models.ManyToManyField(Exercises)

