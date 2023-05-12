from rest_framework.routers import SimpleRouter
from .views import *


router=SimpleRouter()
router.register('customer',CustomerViewSet,basename='customer')
router.register('loyalty',LoyaltyViewSet,basename='loyalty')
router.register('image_database',ImageDatabaseViewSet,basename='ImageDatabase')
router.register('customer_tansaction',CustomerTransactionsViewSet,basename='Customer Transactions')
router.register('auth',AutheticationViewSet,basename='authetication')


