from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
  path('', views.HomeView.as_view()),
  path('striker/', views.HomeView.as_view()),
  path('striker/strikes/<int:pk>/', views.strike_detail, name='strike.detail' ),
  path('striker/strikes/delete-strike/<int:pk>/', views.delete_strike, name='delete-strike'),
  path('striker/strikes/', views.strike_list, name='strike.list'),
  path('striker/strikes/<int:pk>/new/', views.strike_list, name='strike.list'),
  path('striker/<int:pk>/delete/', views.StrikeDeleteView.as_view(), name='strike.delete' ),
  path('striker/import/confirm', views.ImportConfirmView.as_view(), name='import.confirm'),
  path('striker/import/', views.import_data, name='import.data'),
  path('striker/players/', views.PlayerListView.as_view(), name='player.list'),
  path('striker/search-player', views.search_player, name='search.player'),
  path('striker/toons/', views.ToonListView.as_view(), name='toon.list'),
  path('striker/toonsR0/', views.ToonListViewR0.as_view(), name='toon.listR0'),
  path('striker/toonsR1/', views.ToonListViewR1.as_view(), name='toon.listR1'),
  path('striker/toonsR6/', views.ToonListViewR6.as_view(), name='toon.listR6'),
  path('striker/toons5s/', views.ToonListView5s.as_view(), name='toon.list5s'),
  path('striker/toons6s/', views.ToonListView6s.as_view(), name='toon.list6s'),
  path('striker/toons7s/', views.ToonListView7s.as_view(), name='toon.list7s'),
  path('striker/toons5sShip/', views.ToonListView5sShip.as_view(), name='toon.list5sShip'),
  path('striker/toons6sShip/', views.ToonListView6sShip.as_view(), name='toon.list6sShip'),
  path('striker/toons7sShip/', views.ToonListView7sShip.as_view(), name='toon.list7sShip'),
  path('striker/players/<int:pk>', views.PlayerDetailView.as_view(), name='player.detail'),
  path('striker/toons/<slug:toonName>/', views.ToonDetailView.as_view(), name='toon.detail'),
  path("__reload__/", include("django_browser_reload.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
