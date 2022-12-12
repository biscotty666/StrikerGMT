from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from Striker import views

router = routers.DefaultRouter()
router.register(r'api/players', views.PlayerViewSet)
router.register(r'api/strikes', views.StrikeViewSet)
router.register(r'api/toons', views.ToonViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('Striker.urls')),
    path('api-auth/', include('rest_framework.urls'), name='rest_framework')
]

urlpatterns += router.urls
