from django.urls import path, include
from . import views
from .views import import_data, strike_create, strike_detail, strike_delete, strike_update

urlpatterns = [
  path('', views.HomeView.as_view()),
  path('strikes/create/', strike_create, name='strike.create'),
  path('strikes/<int:pk>/', strike_detail, name='strike.detail' ),
  path('strikes/<int:pk>/update/', strike_update, name='strike.update' ),
  path('<int:pk>/delete/', strike_delete, name='strike.delete' ),
  path('import/confirm', views.ImportConfirmView.as_view(), name='import.confirm'),
  path('import/', import_data, name='import.data'),
  path('players/', views.PlayerListView.as_view(), name='player.list'),
  path('strikes/', views.StrikeListView.as_view(), name='strike.list'),
  path('strikes/new', views.StrikeCreateView.as_view(), name='strike.new'),
  path('players/<int:pk>', views.PlayerDetailView.as_view(), name='player.detail'),
  path("__reload__/", include("django_browser_reload.urls")),
]