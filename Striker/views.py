from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, QueryDict
from django.db.models import Count
from .models import Player, Strike, Guild, Toon
from datetime import date, timedelta
from .forms import PlayerModelForm, StrikeModelForm, StrikeForm
from django.views.generic import CreateView, TemplateView, ListView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy

class HomeView(TemplateView):
  template_name = 'Striker/home.html'
  
class ImportConfirmView(TemplateView):
  template_name = 'Striker/import_confirm.html'
  
class StrikeDeleteView(DeleteView):
  model = Strike
  success_url = reverse_lazy('strike.list')

class StrikeUpdateView(UpdateView):
  model = Strike
  fields = ['player', 'strike_date', 'activity', 'ishard', 'comments']
  template_name_suffix = '_update_form'
  success_url = reverse_lazy('strike.list')
  

def strike_update(request, pk):
  strike = Strike.objects.get(id=pk)
  form = StrikeModelForm(instance=strike)
  if request.method == "POST":
    print('Receiving a post request')
    form = StrikeModelForm(request.POST, instance=strike)
    if form.is_valid():
      form.save()
      return redirect('/striker/strikes')
  context = {
    "strike": strike,
    "form": form
  }
  return render(request, "Striker/strike_update.html", context)
  

  
class StrikeCreateView(CreateView):
  model = Strike
  fields = ['player', 'strike_date', 'activity', 'ishard', 'comments']
  success_url = '/striker/strikes'

class PlayerListView(ListView):
  model = Player
  context_object_name = 'players'
  ordering = ['-gp']

# class StrikeListView(ListView):
#   template_name = 'Striker/strikes.html'
#   model = Strike
#   context_object_name = 'strikes'
  
def strike_list(request, **pk):
  strikes = Strike.objects.all().order_by('player')
  if request.method == 'POST':
    if len(pk) == 0:
      form = StrikeModelForm(request.POST)
      if form.is_valid():
        form.save()
        strikes = Strike.objects.all()
        context = {'form': form, 'strikes': strikes}
        return render(request, 'Striker/partials/success.html')
      else:
        return render(request, 'Striker/partials/failure.html')
    else:
      pk = pk['pk']
      strike, created = Strike.objects.get_or_create(id=pk)
      body = request.body.decode("UTF-8")
      result = dict((a.strip(), b.strip())
                    for a, b in (element.split('=') 
                                 for element in body.split('&')))
      player = Player.objects.get(id=result['player'])
      strike.player = player
      strike.strike_date = result['strike_date']
      strike.activity = result['activity']
      ishard = True if 'ishard' in result else False
      strike.ishard = ishard
      strike.comments = result['comments']
      strike.save()
  form = StrikeModelForm()
  strikes = Strike.objects.all().order_by('player')
  counts = Player.objects.annotate(player_strikes = Count('strike')).order_by('-player_strikes')
  context = {'form': form, 'strikes': strikes, 'counts': counts}
  return render(request, "Striker/strikes.html", context)
  
def strike_detail(request, pk):
  strike = get_object_or_404(Strike, pk=pk)
  form = StrikeModelForm(instance=strike)
  context = {'strike': strike, 'form': form}
  if request.method == 'GET':
    return render(request, 'Striker/strike.html', context)
  if request.method == 'PUT':
    data = QueryDict(request.body).dict()
    form = StrikeModelForm(data, instance=strike)
    context = {'strike':strike, 'form':form}
    if form.is_valid():
      form.save()
      return render(request, 'Striker/strikes.html', context)        
      # return render(request, 'Striker/partials/strike-details.html', context)        
    context = {'form':form}
    return render(request, 'Striker/partials/edit-strike-form.html', context)

def delete_strike(request, pk):
  strike = Strike.objects.get(pk=pk) 
  print(strike)
  strike.delete()
  strikes = Strike.objects.all()
  context = {'strikes': strikes}
  # request.user.strike.remove(pk)
  return render(request, 'Striker/partials/strike-list.html', context)

class ToonListView(ListView):
  def get_queryset(self):
    queryset = Toon.objects.filter(gearLevel__gt=11)
    queryset = queryset.values('toonName').annotate(toonNameCount=(Count('toonName'))).order_by('toonName')
    return queryset
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['Label'] = 'G12+'
    return context
  context_object_name = 'toonsCount'

class ToonListViewR0(ListView):
  def get_queryset(self):
    queryset = Toon.objects.filter(gearLevel__gt=12)
    queryset = queryset.values('toonName').annotate(toonNameCount=(Count('toonName'))).order_by('toonName')
    return queryset
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['Label'] = 'G13+'
    return context
  context_object_name = 'toonsCount'
class ToonListViewR1(ListView):
  def get_queryset(self):
    queryset = Toon.objects.filter(gearLevel__gt=13)
    queryset = queryset.values('toonName').annotate(toonNameCount=(Count('toonName'))).order_by('toonName')
    return queryset
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['Label'] = 'R1+'
    return context
  context_object_name = 'toonsCount'

class ToonListViewR2(ListView):
  def get_queryset(self):
    queryset = Toon.objects.filter(gearLevel__gt=14)
    queryset = queryset.values('toonName').annotate(toonNameCount=(Count('toonName'))).order_by('toonName')
    return queryset
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['Label'] = 'R2+'
    return context
  context_object_name = 'toonsCount'

class ToonListViewR3(ListView):
  def get_queryset(self):
    queryset = Toon.objects.filter(gearLevel__gt=11)
    queryset = queryset.values('toonName').annotate(toonNameCount=(Count('toonName'))).order_by('toonName')
    return queryset
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['Label'] = 'R3+'
    return context
  context_object_name = 'toonsCount'

class ToonListViewR4(ListView):
  def get_queryset(self):
    queryset = Toon.objects.filter(gearLevel__gt=11)
    queryset = queryset.values('toonName').annotate(toonNameCount=(Count('toonName'))).order_by('toonName')
    return queryset
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['Label'] = 'R4+'
    return context
  context_object_name = 'toonsCount'

class ToonListViewR5(ListView):
  def get_queryset(self):
    queryset = Toon.objects.filter(gearLevel__gt=11)
    queryset = queryset.values('toonName').annotate(toonNameCount=(Count('toonName'))).order_by('toonName')
    return queryset
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['Label'] = 'R5+'
    return context
  context_object_name = 'toonsCount'

class ToonListViewR6(ListView):
  def get_queryset(self):
    queryset = Toon.objects.filter(gearLevel__gt=11)
    queryset = queryset.values('toonName').annotate(toonNameCount=(Count('toonName'))).order_by('toonName')
    return queryset
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['Label'] = 'R6+'
    return context
  context_object_name = 'toonsCount'

class ToonListViewR7(ListView):
  def get_queryset(self):
    queryset = Toon.objects.filter(gearLevel__gt=11)
    queryset = queryset.values('toonName').annotate(toonNameCount=(Count('toonName'))).order_by('toonName')
    return queryset
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['Label'] = 'R7+'
    return context
  context_object_name = 'toonsCount'

class ToonListViewR8(ListView):
  def get_queryset(self):
    queryset = Toon.objects.filter(gearLevel__gt=11)
    queryset = queryset.values('toonName').annotate(toonNameCount=(Count('toonName'))).order_by('toonName')
    return queryset
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['Label'] = 'R8+'
    return context
  context_object_name = 'toonsCount'

class ToonListViewR9(ListView):
  def get_queryset(self):
    queryset = Toon.objects.filter(gearLevel__gt=11)
    queryset = queryset.values('toonName').annotate(toonNameCount=(Count('toonName'))).order_by('toonName')
    return queryset
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['Label'] = 'R9'
    return context
  context_object_name = 'toonsCount'


class ToonListView5s(ListView):
  def get_queryset(self):
    queryset = Toon.objects.filter(rarity__gt=5)
    queryset = queryset.values('toonName').annotate(toonNameCount=(Count('toonName'))).order_by('toonName')
    return queryset
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['Label'] = '5\u2B50+'
    return context
  context_object_name = 'toonsCount'

class ToonListView6s(ListView):
  def get_queryset(self):
    queryset = Toon.objects.filter(rarity__gt=6)
    queryset = queryset.values('toonName').annotate(toonNameCount=(Count('toonName'))).order_by('toonName')
    return queryset
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['Label'] = '6\u2B50+'
    return context
  context_object_name = 'toonsCount'

class ToonListView7s(ListView):
  def get_queryset(self):
    queryset = Toon.objects.filter(rarity=7)
    print(queryset.values('toonLevel'))
    queryset = queryset.values('toonName').annotate(toonNameCount=(Count('toonName'))).order_by('toonName')
    return queryset
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['Label'] = '7\u2B50'
    return context
  context_object_name = 'toonsCount'

class PlayerDetailView(DetailView):
  model = Player
  context_object_name = 'player'
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['toons'] = Toon.objects.filter(player=self.kwargs['pk']).filter(gearLevel__gt=1).order_by('-gp')
    context['ships'] = Toon.objects.filter(player=self.kwargs['pk']).exclude(gearLevel__gt=1).order_by('-gp')
    return context

class ToonDetailView(DetailView):
  model = Toon
  # toons = Toon.objects.filter(player=pk_url_kwarg)
  context_object_name = 'toon'
  slug_field = 'toonName'
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    # print(self.kwargs)
    context['players'] = Toon.objects.filter(toon=self.kwargs['toonName']).order_by('toonName')
    return context
      
def import_data(request):
  from .swgohhelp import SWGOHhelp, settings
  import json
  with open('Striker/swgoh/json/config.json') as f:
    config = json.load(f)

  creds = settings(config['credname'], config['credpass'], config['crednum'], config['credlet'])
  client = SWGOHhelp(creds)

  print("Getting player game data...")
  def get_response():
    try:
      print("Trying guild endpoint")
      return client.get_data('guild', config['allycode'])
    except Exception as e:
      print('Bad response, trying again...')
      get_response()
  response = get_response()
  roster = response[0]['roster']
  new_guild = response[0]
  
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
  else:
    guild = Guild.objects.get(pk='1')
    guild.name = new_guild['name']
    guild.desc = new_guild['desc']
    guild.members = new_guild['members']
    guild.status = new_guild['status']
    guild.required = new_guild['required']
    guild.bannerColor = new_guild['bannerColor']
    guild.bannerLogo = new_guild['bannerLogo']
    guild.message = new_guild['message']
    guild.gp = new_guild['gp']
    
  all_players = Player.objects.all()
  for player in all_players:
    if player not in roster:
      player.active = False
      
  for player in roster:
    new_player = player['id']
    if Player.objects.filter(playerId=new_player).exists():
      existing_player = Player.objects.get(playerId=new_player)
      existing_player.gp=player['gp']
      existing_player.allycode=player['allyCode']
      existing_player.level=player['level']
      existing_player.gpChar=player['gpChar']
      existing_player.gpShip=player['gpShip']
      existing_player.name=player['name']
      existing_player.active=True
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
  import time

  for player in players:
    print("Getting toon game data...")
    def GetData():
      try:
        print(f'Trying player endpoint for {player.name}, {player.allycode}')
        response = client.get_data('player', player.allycode)
        return response
      except Exception as e:
        print("No response. Napping for 15...")
        time.sleep(15)
        GetData()
    response = GetData()
    print(f"Got data for {player}")

    try:
      roster = response[0]['roster']
    except:
      GetData()

    for toon in roster:
      relic = toon['relic']
      
      if toon['relic']==None or toon['relic']['currentTier']==1:
        relic=0
      else:
        relic=toon['relic']['currentTier']-2
      if toon['primaryUnitStat']==None:
        pus=0
      else:
        pus=toon['primaryUnitStat']      
      all_toons = Toon.objects.all()
      new_toon = Toon(
          player = player,
          toonID = toon['id'],
          toonName= toon['defId'],
          nameKey = toon['nameKey'],
          rarity = toon['rarity'],
          toonLevel = toon['level'],
          gp = toon['gp'],
          gearLevel = toon['gear'],
          combatType = toon['combatType'],
          primaryUnitStat = pus,
          relic = relic,
       )    
      new_toon.save()
      print(f"{new_toon.toonName} saved")

  return render(request, 'Striker/import_success.html')