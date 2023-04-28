from asyncio.windows_events import NULL
from secrets import choice
from turtle import ondrag
from unicodedata import category
from unittest.util import _MAX_LENGTH
from django.db import models
from User.models import Users

# Create your models here.

ALUNMS_CATEGORY = (
        ("1", "Principiante"),
        ("2", "Experiencia Previa"),
        ("3", "Avanzado")
    )

class physicalReports(models.Model):
    id                          = models.AutoField(primary_key = True)
    dateEvaluation              = models.DateField(null = False)
    objetive                    = models.CharField(max_length = 100, null = False)
    age                         = models.IntegerField(null = False)
    heightCM                    = models.IntegerField(null = False)
    cellPhoneNumber             = models.CharField(max_length = 12, null = False)
    cellPhoneNumberEmergency    = models.CharField(max_length = 12, null = False)
    operations                  = models.CharField(max_length = 250, null = True)
    musclePains                 = models.CharField(max_length = 250, null = True)
    sickness                    = models.CharField(max_length = 250, null = True)
    posturalProblems            = models.CharField(max_length = 250, null = True)
    injuries                    = models.CharField(max_length = 250, null = True)
    categoryAlumn               = models.CharField(choices = ALUNMS_CATEGORY, null = False, max_length = 20)
    weight                      = models.FloatField(null = False)
    AT                          = models.FloatField(null = False)
    ATKG                        = models.FloatField(null = False)
    percentageOfWater           = models.FloatField(null = False) 
    ATKG                        = models.FloatField(null = False)
    muscleMassKG                = models.FloatField(null = False)
    valuationPhysical           = models.CharField(max_length = 50, null = False)
    tmb                         = models.CharField(max_length = 250, null = False)
    biologicalAge               = models.IntegerField(null = True)
    boneMass                    = models.FloatField(null = True)
    visceralFat                 = models.CharField(null = True, max_length = 100)
    imc                         = models.CharField(null = True, max_length = 100)
    trainer                     = models.ForeignKey(Users, on_delete = models.PROTECT, related_name = "trainer_physicalReport_set")
    member                      = models.ForeignKey(Users, on_delete = models.PROTECT, related_name = "member_physicalReport_set")


