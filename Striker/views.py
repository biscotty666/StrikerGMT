from django.shortcuts import render
from django.http import HttpResponse

from .models import Player, Strike, Guild, Toon
from datetime import date, timedelta
from .forms import PlayerModelForm
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
  ordering = ['-gp']

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

def import_data(request):
  from .swgohhelp import SWGOHhelp, settings
  import json
  with open('Striker/swgoh/json/config.json') as f:
    config = json.load(f)

  creds = settings(config['credname'], config['credpass'], config['crednum'], config['credlet'])
  client = SWGOHhelp(creds)

  print("Getting player game data...")
  response = client.get_data('guild', config['allycode'])
  with open('Striker/swgoh/json/guild.json', 'w') as f:
    json.dump(response, f)

  print("Getting toon game data...")
  response = client.get_data('player', config['allycode'])
  with open('Striker/swgoh/json/player.json', 'w') as f:
    json.dump(response, f)
  
  with open('Striker/swgoh/json/guild.json', 'r') as f:
    guild = json.load(f)
    roster = guild[0]['roster']
  
  if Guild.objects.filter(pk='1') == False:  
    new_guild = Guild(
      guildId = guild['id'],
      name = guild['name'],
      desc = guild['desc'],
      members = guild['members'],
      status = guild['status'],
      required = guild['required'],
      bannerColor = guild['bannerColor'],
      bannerLogo = guild['bannerLogo'],
      message = guild['message'],
      gp = guild['gp'],
    )
    new_guild.save()
    
  all_players = Player.objects.all()
  for player in all_players:
    if player not in roster:
      player.active = False
      
  for player in roster:
    new_player = player['name']
    if Player.objects.filter(name=new_player).exists():
      existing_player = Player.objects.get(name=new_player)
      existing_player.gp=player['gp']
      existing_player.allycode=player['allyCode']
      existing_player.level=player['level']
      existing_player.gpChar=player['gpChar']
      existing_player.gpShip=player['gpShip']
      existing_player.playerId=player['id']
      existing_player.save()
      print('player updated')       
    else:
      new_player = Player(
        name=player['name'],
        playerId=player['id'],
        gp=player['gp'],
        allycode=player['allyCode'],
        level=player['level'],
        gpChar=player['gpChar'],
        gpShip=player['gpShip'],
        active=True,
        guildMemberLevel=player['guildMemberLevel'],
        updated=player['updated'],
      )
      new_player.save()
      print('New player saved')

  print('Import toons')
  players = Player.objects.all()
  Toon.objects.all().delete()
  for player in players:
    with open('Striker/swgoh/json/player.json') as f:
      roster = json.load(f)
      roster = roster[0]['roster']
      for toon in roster:
        relic = toon['relic']
        if toon['relic']==None:
          relic=0
        else:
          relic=toon['relic']['currentTier']
        if toon['primaryUnitStat']==None:
          pus=0
        else:
          pus=toon['primaryUnitStat']      
        all_toons = Toon.objects.all()
        if toon not in all_toons and toon['gear']>1:
          new_toon = Toon(
            player = player,
            toonID = toon['id'],
            toonName= toon['defId'],
            nameKey = toon['nameKey'],
            rarity = toon['rarity'],
            toonLevel = toon['level'],
            gp = toon['gp'],
            gearLevel = toon['gear'],
            primaryUnitStat = pus,
            relic = relic
          )    
          new_toon.save()
          
    print(player)

  return render(request, 'Striker/import_success.html')
