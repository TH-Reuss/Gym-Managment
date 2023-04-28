"""appgym URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from User import views as usersViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('planDeEjercicio/', include('planDeEjercicio.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    path('api/users/', include('User.urls')),
    path('api/gyms/', include('Gym.urls')),
    path('adminLogin/', usersViews.login),
    path('select_gym', usersViews.select_gym, name = "select_gym"),
    path('manage_gym/<int:id>', usersViews.manage_gym, name="manage_gym"),
    path('logout/', usersViews.signout),
    path('members/<int:id_gym>', usersViews.members, name="members"),
    path('members/create/<int:id_gym>', usersViews.create_member, name="create_member"),
    path('members/disable/<int:id_gym>/<int:id_member>/', usersViews.disable_member, name = "disable_member"),
    path('members/enable/<int:id_gym>/<int:id_member>/', usersViews.enable_member, name = "enable_member"),
    path('members/update/<int:id_gym>/<int:id_user>', usersViews.update_user, name="update_member"),
    path('trainers/<int:id_gym>', usersViews.trainers, name="trainers"),
    path('trainers/create/<int:id_gym>', usersViews.create_trainer, name="create_trainer"),
    path('trainers/update/<int:id_gym>/<int:id_user>', usersViews.update_user, name="update_trainer"),
    path('trainers/disable/<int:id_gym>/<int:id_trainer>/', usersViews.disable_trainer, name = "disable_trainer"),

    #borrar despues
    path('test/getUserByToken', usersViews.getUser),
]

