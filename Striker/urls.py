from django.urls import path
from . import views

urlpatterns = [
  path('', views.HomeView.as_view()),
  path('players/', views.PlayerListView.as_view(), name='player.list'),
  path('strikes/', views.StrikeListView.as_view(), name='strike.list'),
  path('strikes/new', views.StrikeCreateView.as_view(), name='strike.new'),
  path('players/<int:pk>', views.PlayerDetailView.as_view(), name='player.detail')
]