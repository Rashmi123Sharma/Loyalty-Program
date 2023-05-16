from rest_framework.routers import SimpleRouter
from .views import *


router=SimpleRouter()
router.register('customer',CustomerViewSet,basename='customer')
router.register('loyalty',LoyaltyViewSet,basename='loyalty')
router.register('image_database',ImageDatabaseViewSet,basename='ImageDatabase')
router.register('customer_tansaction',CustomerTransactionsViewSet,basename='Customer Transactions')
router.register('get_otp',GetOtpViewSet,basename='get_otp')
router.register('verify_otp',VerifyOtpViewSet,basename='verify_otp')
router.register('resend_otp',ResendOtpViewSet,basename='resend_otp')
router.register('dashboard_user',DashboardUserViewSet,basename='dashboard_user')


