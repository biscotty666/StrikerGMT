from django.urls import path, include
from . import views
from .views import import_data

urlpatterns = [
  path('', views.HomeView.as_view()),
  path('import/', import_data, name='import-data'),
  path('players/', views.PlayerListView.as_view(), name='player.list'),
  path('strikes/', views.StrikeListView.as_view(), name='strike.list'),
  path('strikes/new', views.StrikeCreateView.as_view(), name='strike.new'),
  path('players/<int:pk>', views.PlayerDetailView.as_view(), name='player.detail'),
  path("__reload__/", include("django_browser_reload.urls")),
]