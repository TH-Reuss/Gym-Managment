from django.urls import path

from . import views

urlpatterns = [
    path('getAllExercisePlans', views.getAllExercisePlans),
    path('getExercisePlan/<int:id>', views.getExercisePlan)
]