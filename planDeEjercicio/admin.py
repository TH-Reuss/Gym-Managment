from django.contrib import admin

import planDeEjercicio
from .models import *
# Register your models here.

class ExercisePlansAdmin(admin.ModelAdmin):
    list_display = ('id', 'Fecha')

    @admin.display(description = "Fecha")
    def Fecha(self, obj):
        return obj.date


class RoutinesAdmin(admin.ModelAdmin):
    fields = ('day', 'description', 'ExercisePlan','image')
    list_display = ('id', 'day', 'description', 'ExercisePlanAdmin')

    @admin.display(description = "Plan de Ejercicio N°")
    def ExercisePlanAdmin(self, obj):
        return obj.ExercisePlan.id

    

admin.site.register(ExercisePlans, ExercisePlansAdmin)
admin.site.register(Routines, RoutinesAdmin)
admin.site.register(Exercises)