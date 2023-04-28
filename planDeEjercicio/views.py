from re import L
from textwrap import indent
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *

# Create your views here.

def getAllExercisePlans(request):
    exercisePlans = list(ExercisePlans.objects.values())
    return JsonResponse(exercisePlans, safe = False)

def getExercisePlan(request, id):
    exercisePlan = ExercisePlans.objects.get(id=id)
    print(exercisePlan)

    exercisePlanJson = {
        "id" : exercisePlan.id,
        "date" : exercisePlan.date
    }
    
    return JsonResponse(exercisePlanJson)