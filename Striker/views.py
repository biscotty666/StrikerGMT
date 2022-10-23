from django.shortcuts import render
from django.http import HttpResponse
from .models import Player, Strike
from datetime import date, timedelta
from django.views.generic import CreateView, TemplateView, ListView, DetailView

class HomeView(TemplateView):
  template_name = 'Striker/home.html'
  
class StrikeCreateView(CreateView):
  model = Strike
  fields = ['player', 'strike_date', 'activity', 'ishard', 'comments']
  success_url = '/strikes/'

class PlayerListView(ListView):
  model = Player
  context_object_name = 'players'

class StrikeListView(ListView):
  model = Strike
  def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ActiveDate = date.today() - timedelta(days=30)
        context['strikes_active'] = Strike.objects.filter(strike_date__gte=ActiveDate).order_by('-strike_date')
        context['strikes_legacy'] = Strike.objects.filter(strike_date__lt=ActiveDate).order_by('-strike_date')
        return context


class PlayerDetailView(DetailView):
  model = Player
  context_object_name = 'player'
