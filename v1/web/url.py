from rest_framework.routers import SimpleRouter
router=SimpleRouter()
from .views import *


router.register('users',UserViewSet,basename='users')
router.register('loyalty',LoyaltyViewSet,basename='loyalty')
router.register('image_database',ImageDatabaseViewSet,basename='IMageDatabase')
router.register('customer_tansaction',CustomerTransactionsViewSet,basename='IMageDatabase')
router.register('auth',OTPViewSet,basename='auth')

