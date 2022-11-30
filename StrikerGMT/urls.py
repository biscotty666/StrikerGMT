from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from Striker import views

router = routers.DefaultRouter()
router.register(r'players', views.PlayerViewSet)
router.register(r'strikes', views.StrikeViewSet)
router.register(r'toons', views.ToonViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/players/', views.PlayerViewSet, name='api-players'),
    path('', include('Striker.urls')),
    path('api-auth/', include('rest_framework.urls'), name='rest_framework')
]

urlpatterns += router.urls
