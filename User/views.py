from email.utils import parseaddr
import imp
from queue import Empty
from urllib import request, response
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, authenticate
from django.contrib.auth import login as login_
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
import pdb

from Gym.models import Gyms
import User
from .models import Administrators, Members, UserType, Users, UsersTypes, Trainers
import json
# Create your views here.

def is_admin(user):
    administrator = Administrators.objects.get(user = user)
    if not administrator:
        return False
    else:
        return True
        

def validate_gym_of_user_admin(id_gym, user):
    administrator = Administrators.objects.get(user = user)
    for gym in administrator.gyms.all():
        if gym.id == id_gym:
            return True

    return False

def validate_type_user_admin(user):
    for typeUser in user.userType.all():
        if typeUser.description == "Administrator":
            return True
    return False

def validate_type_user_member(user):
    for typeUser in user.userType.all():
        if typeUser.description == "Member":
            return True
    return False

def login(request):
    #buscar elemento en una lista
    if request.method == 'GET':
        return render(request, 'adminLogin.html')
    else:
        print(request.POST['username'])
        print(request.POST['password'])
        administrator = authenticate(username = request.POST['username'], password = request.POST['password'])
        print(administrator)
        if administrator is not None:
            print("Logeado Correctamente")
            login_(request, administrator)
            return redirect('select_gym')
        else:
            return render(request, 'adminLogin.html',
            {
                "error" : "Las credenciales son incorrectas"
            })

def select_gym(request):
    user = request.user
    if user.is_authenticated and is_admin(user):
        gyms_administrator = Administrators.objects.get(user = user).gyms.all()
        return render(request, 'select_gym.html', {"gyms" : gyms_administrator})
    else:
        return HttpResponse("Necesita Iniciar Sesión con una cuenta de administrador")

def manage_gym(request, id):
    user = request.user
    if user.is_authenticated and is_admin(user):
        if validate_gym_of_user_admin(id_gym = id, user = user):
            return render(request, 'dashboard.html', {
                "user" : user,
                "gym" : Gyms.objects.get(id = id)
                })
        else:
            return HttpResponse("La cuenta de administrador no tiene acceso a este gimnasio, no haga eso") 
    else:
        return HttpResponse("Necesita Iniciar Sesión con una cuenta de administrador")
    
def signout(request):
    logout(request)
    return redirect('/adminLogin')


def members(request, id_gym):
    user = request.user
    if user.is_authenticated and is_admin(user):
        if validate_gym_of_user_admin(id_gym = id_gym, user = user):
            members = Members.objects.filter(gyms = id_gym)
            return render(request, 'members.html',{
                "members" : members,
                "gym" : Gyms.objects.get(id = id_gym)
            })
        else:
            return HttpResponse("La cuenta de administrador no tiene acceso a este gimnasio, no haga eso")
    else:
        return HttpResponse("Necesita Iniciar Sesión con una cuenta de administrador")

def create_member(request, id_gym):
    user = request.user
    if user.is_authenticated and is_admin(user):
        if validate_gym_of_user_admin(id_gym = id_gym, user = user):
            if request.method == 'GET':
                return render(request, 'create_member.html', {"gym" : Gyms.objects.get(id = id_gym)})
            else:
                gym_form = Gyms.objects.get(name = request.POST['gym_name'])
                user, is_created = Users.objects.get_or_create(
                    rut         = request.POST['rut'],
                    defaults    = {
                        'first_name' : request.POST['first_name'],
                        'last_name'  : request.POST['last_name'],
                        'gender'     : request.POST['gender'],
                        'birthday'   : request.POST['birthday'],
                        'email'      : request.POST['user'] + "@" + request.POST['domain'],
                        'username'   : request.POST['rut'],
                        'password'   : request.POST['rut'].split('-')[0][-4:],
                        'is_active'  : True,
                    }
                )
                #recien se creo el usuario
                if is_created == True:
                    user.set_password(request.POST['rut'].split('-')[0][-4:])
                    user.save()
                    member = Members(
                        user        = user
                    )
                    member.gyms.add(gym_form)
                    member.save()
                    return redirect("members", id_gym = id_gym)
                else:
                    member, is_created = Members.objects.get_or_create(
                        user        = user,
                    )
                    
                    member.gyms.add(gym_form)
                    member.save()
                    return redirect("members", id_gym = id_gym)
                    
        return HttpResponse("La cuenta de administrador no tiene acceso a este gimnasio, no haga eso")
    else:
        return HttpResponse("Necesita Iniciar Sesión con una cuenta de administrador")

def disable_member(request, id_gym, id_member):
    user = request.user
    if user.is_authenticated and is_admin(user):
        if validate_gym_of_user_admin(id_gym = id_gym, user = user):
            if request.method == 'GET':
                member = Members.objects.get(user__id = id_member)
                member.gyms.remove(id_gym)
                member.save()
                return redirect("members", id_gym = id_gym)
            else:
                return HttpResponse("Metodo no aceptado")
        else:
            return HttpResponse("La cuenta de administrador no tiene acceso a este gimnasio, no haga eso")
    else:
        return HttpResponse("Necesita Iniciar Sesión con una cuenta de administrador")

def enable_member(request, id_gym, id_member):
    user = request.user
    if user.is_authenticated and is_admin(user):
        if validate_gym_of_user_admin(id_gym = id_gym, user = user):
            if request.method == 'GET':
                member = Members.objects.get(user__id = id_member)
                member.user.add(id_gym)
                member.save()
                return redirect("members", id_gym = id_gym)
            else:
                return HttpResponse("Metodo no aceptado")
        else:
            return HttpResponse("La cuenta de administrador no tiene acceso a este gimnasio, no haga eso")
    else:
        return HttpResponse("Necesita Iniciar Sesión con una cuenta de administrador")

def update_user(request, id_gym, id_user):
    user = request.user
    if request.user.is_authenticated and is_admin(user):
        if validate_gym_of_user_admin(id_gym = id_gym, user = user):
            if request.method == 'GET':
                user = Users.objects.get(id = id_user)
                email = user.email.split("@")
                username = email[0]
                domain = email[1]

                print(request.path_info)
                return render(request, 'update_user.html', {
                    "user": user,
                    "user_birthday" : user.birthday.strftime("%Y-%m-%d"),
                    "user_user"     : username,
                    "user_domain"   : domain,
                    "gym"           : Gyms.objects.get(id = id_gym)
                    })
            else:
                user = Users.objects.get(id = id_user)

                user.first_name   = request.POST['first_name']
                user.last_name    = request.POST['last_name']
                user.gender       = request.POST['gender']
                user.birthday     = request.POST['birthday']
                user.email        = request.POST['user'] + "@" + request.POST['domain']
                user.set_password(request.POST['rut'].split('-')[0][-4:])
                user.save()

                return redirect(request.path_info)  
        else:
            return HttpResponse("La cuenta de administrador no tiene acceso a este gimnasio, no haga eso")

    else:
        return HttpResponse("Necesita Iniciar Sesión con una cuenta de administrador")

def disable_user(request, id):
    if request.user.is_authenticated and request.user.userType == "1":
        if request.method == 'GET':
            user = Users.objects.get(id = id)
            user.is_active = False
            user.save()

            if user.userType == "3":
                return redirect('members')
            elif user.userType == "2":
                return redirect('trainers')
            
        else:
            return HttpResponse("Metodo no admitido")

    else:
        return HttpResponse("Necesita Iniciar Sesión con una cuenta de administrador")

def enable_user(request, id):
    if request.user.is_authenticated and request.user.userType == "1":
        if request.method == 'GET':
            user = Users.objects.get(id = id)
            user.is_active = True
            user.save()

            print(user)
            if user.userType == "3":
                return redirect('members')
            elif user.userType == "2":
                return redirect('trainers')
            
        else:
            return HttpResponse("Metodo no admitido")

    else:
        return HttpResponse("Necesita Iniciar Sesión con una cuenta de administrador")

def trainers(request, id_gym):
    user = request.user
    if user.is_authenticated and is_admin(user):
        if validate_gym_of_user_admin(id_gym = id_gym, user = user):
            trainers = Trainers.objects.filter(gyms = id_gym)
            return render(request, 'trainers.html',{
                "trainers" : trainers,
                "gym" : Gyms.objects.get(id = id_gym)
            })
    else:
        return HttpResponse("Necesita Iniciar Sesión con una cuenta de administrador")

def create_trainer(request, id_gym):
    user = request.user
    if user.is_authenticated and is_admin(user):
        if validate_gym_of_user_admin(id_gym = id_gym, user = user):
            if request.method == 'GET':
                return render(request, 'create_trainer.html', {"gym" : Gyms.objects.get(id = id_gym)})
            else:
                gym_form = Gyms.objects.get(name = request.POST['gym_name'])
                user, is_created = Users.objects.get_or_create(
                    rut         = request.POST['rut'],
                    defaults    = {
                        'first_name' : request.POST['first_name'],
                        'last_name'  : request.POST['last_name'],
                        'gender'     : request.POST['gender'],
                        'birthday'   : request.POST['birthday'],
                        'email'      : request.POST['user'] + "@" + request.POST['domain'],
                        'username'   : request.POST['rut'],
                        'password'   : request.POST['rut'].split('-')[0][-4:],
                        'is_active'  : True,
                    }
                )
                #recien se creo el usuario
                if is_created == True:
                    user.set_password(request.POST['rut'].split('-')[0][-4:])
                    user.save()
                    trainer = Trainers(
                        user        = user
                    )
                    trainer.gyms.add(gym_form)
                    trainer.save()
                    return redirect("trainers", id_gym = id_gym)
                else:
                    trainer, is_created = Trainers.objects.get_or_create(
                        user        = user,
                    )
                    
                    trainer.gyms.add(gym_form)
                    trainer.save()
                    return redirect("trainers", id_gym = id_gym)
                    
        return HttpResponse("La cuenta de administrador no tiene acceso a este gimnasio, no haga eso")
    else:
        return HttpResponse("Necesita Iniciar Sesión con una cuenta de administrador")

def disable_trainer(request, id_gym, id_trainer):
    user = request.user
    if user.is_authenticated and is_admin(user):
        if validate_gym_of_user_admin(id_gym = id_gym, user = user):
            if request.method == 'GET':
                trainer = Trainers.objects.get(user__id = id_trainer)
                trainer.gyms.remove(id_gym)
                trainer.save()
                return redirect("trainers", id_gym = id_gym)
            else:
                return HttpResponse("Metodo no aceptado")
        else:
            return HttpResponse("La cuenta de administrador no tiene acceso a este gimnasio, no haga eso")
    else:
        return HttpResponse("Necesita Iniciar Sesión con una cuenta de administrador")

#Borrar despues
def getUser(request):
    if request.method == 'POST':
        userToken = request.POST['Token']
        user_id = Token.objects.get(key=userToken).user_id
        user = User.objects.get(id=user_id)

        informacion_usuario = {
            "first_name" : user.first_name
        }
        return JsonResponse(informacion_usuario)
    else:
        HttpResponse("Metodo no disponible")

