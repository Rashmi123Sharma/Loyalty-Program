from rest_framework.routers import SimpleRouter
router=SimpleRouter()
from .views import *


router.register('data',UserViewSet,basename='data')
router.register('loyalty',LoyaltyViewSet,basename='loyalty')
router.register('image_database',ImageDatabaseViewSet,basename='IMageDatabase')

