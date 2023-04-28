from argparse import Action
from .models import Gyms
from rest_framework import viewsets, permissions
from .serializers import GymsSerializer

class GymsViewset(viewsets.ModelViewSet):
    queryset = Gyms.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = GymsSerializer