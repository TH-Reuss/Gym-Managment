from rest_framework import routers
from .api import GymsViewset

router = routers.DefaultRouter()

router.register('', GymsViewset)

urlpatterns = router.urls