from telnetlib import STATUS
from urllib import response
from rest_framework.decorators import action
import User
from User.models import UserType, Users
from rest_framework import viewsets, permissions
from .serializers import UsersSerializer
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import status
from Gym.models import *
from .models import *
from planDeEjercicio.models import *
from django.core import serializers
import pdb

class UsersViewset(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    serializer_class = UsersSerializer

    @action(detail = False, methods = ['post'])
    def createMember(self, request):

        user_id         = Token.objects.get(key = request.auth.key).user_id
        user            = Users.objects.get(id = user_id)
        
        if user.userType == "1":
            administrator = user
        else:
            content = "the token does not correspond to an administrator"
            return Response(content, status = status.HTTP_400_BAD_REQUEST)

        Member_serializer = UsersSerializer(data = request.data)

        if Member_serializer.is_valid():
            member = Users(
                username    = Member_serializer.validated_data['username'],
                password    = Member_serializer.validated_data['password'],
                email       = Member_serializer.validated_data['email'],
                gym         = administrator.gym,
                rut         = Member_serializer.validated_data['rut'],
                first_name  = Member_serializer.validated_data['first_name'],
                last_name   = Member_serializer.validated_data['last_name'],
                is_active   = Member_serializer.validated_data['is_active'],
                userType    = Member_serializer.validated_data['userType'],
            )
            member.save()
            content = "user created successfully"
            return Response(content, status = status.HTTP_201_CREATED)

        else:
            return Response(Member_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    @action(detail = False, methods = ['post'])
    def getUserByToken(self, request):
        if request.method == 'POST':
            userToken = request.POST['Token']
            user_id = Token.objects.get(key=userToken).user_id
            user = Users.objects.get(id=user_id)

            informacion_usuario = {
                "first_name" : user.first_name,
                "last_name"  : user.last_name
            }
            return JsonResponse(informacion_usuario)
        else:
            HttpResponse("Metodo no disponible")

    @action(detail=False, methods = ['post'])
    def getExercisePlansFromUser(self, request):

        userToken = request.data['Token']

        user_id = Token.objects.get(key=userToken).user_id
        user = Users.objects.get(id=user_id)
        member = Members.objects.get(user = user)

        exercisePlans = ExercisePlans.objects.filter(member = member)
        data = list()
        for exercisPlan in exercisePlans:
            data.append({
                "id"        : exercisPlan.id,
                "date"      : exercisPlan.date
            })

        
        #exercisePlans_json = serializers.serialize('json', exercisePlans, indent = 4)
        #print(exercisePlans_json)
        return JsonResponse(data, safe=False)

    @action(detail=False, methods = ['post'])
    def getRoutineFromExercisePlan(self, request):
        exercisePlanID = request.data['exercisePlan']
        exercisePlan = ExercisePlans.objects.get(id = exercisePlanID)
        routines = Routines.objects.filter(ExercisePlan = exercisePlan)
        
        data = list()
        for routine in routines:
            data.append({
                "id": routine.id,
                "description": routine.description,
                "day": routine.get_day_display(),
                "image": routine.image
            })
        
        return JsonResponse(data, safe=False)