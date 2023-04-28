from rest_framework import routers
from .api import UsersViewset

router = routers.DefaultRouter()

router.register('', UsersViewset)

urlpatterns = router.urls