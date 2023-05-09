from django.contrib import admin
from django.urls import path,include
from v1.web.url import router as web_router
from v1.app.url import router as app_router
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/web/',include(web_router.urls)),
    path('v1/app/',include(app_router.urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
