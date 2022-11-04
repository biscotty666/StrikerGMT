from django.urls import path, include
from . import views
from .views import import_data, strike_update

urlpatterns = [
  path('', views.HomeView.as_view()),
  path('striker/', views.HomeView.as_view()),
  path('striker/strikes/create/', views.StrikeCreateView.as_view(), name='strike.create'),
  path('striker/strikes/<int:pk>/', views.StrikeDetailView.as_view(), name='strike.detail' ),
  path('striker/strikes/<int:pk>/update/', views.StrikeUpdateView.as_view(), name='strike.update' ),
  # path('striker/strikes/<int:pk>/update/', strike_update, name='strike.update' ),
  path('striker/<int:pk>/delete/', views.StrikeDeleteView.as_view(), name='strike.delete' ),
  path('striker/import/confirm', views.ImportConfirmView.as_view(), name='import.confirm'),
  path('striker/import/', import_data, name='import.data'),
  path('striker/players/', views.PlayerListView.as_view(), name='player.list'),
  path('striker/strikes/', views.StrikeListView.as_view(), name='strike.list'),
  path('striker/toons/', views.ToonListView.as_view(), name='toon.list'),
  path('striker/toons5s/', views.ToonListView5s.as_view(), name='toon.list5s'),
  path('striker/toons6s/', views.ToonListView6s.as_view(), name='toon.list6s'),
  path('striker/toons7s/', views.ToonListView7s.as_view(), name='toon.list7s'),
  path('striker/strikes/new', views.StrikeCreateView.as_view(), name='strike.new'),
  path('striker/players/<int:pk>', views.PlayerDetailView.as_view(), name='player.detail'),
  path('striker/toons/<slug:toonName>/', views.ToonDetailView.as_view(), name='toon.detail'),
  path("__reload__/", include("django_browser_reload.urls")),
]