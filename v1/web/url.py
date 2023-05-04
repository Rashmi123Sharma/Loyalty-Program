from rest_framework.routers import SimpleRouter
router=SimpleRouter()
from .views import *


router.register('data',UserViewSet,basename='data')

