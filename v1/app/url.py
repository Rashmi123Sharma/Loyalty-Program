from rest_framework.routers import SimpleRouter
from .views import *
router=SimpleRouter()


# urlpatterns = [
#     path('signup', SignUp, name='signup'),
#     # path('userprofile/',UserProfileView , name='userprofile'),
#     # path('userprofile/<int:user_id>/',UserProfileView , name='userprofile'),
# ]

router.register('signup',SignUp,basename = 'signup')
router.register('userprofile',UserProfileView,basename = 'userprofile')