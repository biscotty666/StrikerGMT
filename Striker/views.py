from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, QueryDict
from django.db.models import Count
from .models import Player, Strike, Guild, Toon, Mod, Skill, ModStat, Equipped, ShipCrew
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
    queryset = Toon.objects.filter(relic__gt=1).exclude(relic__gt=6)
    queryset = queryset.values('toonName').annotate(toonNameCount=(Count('toonName'))).order_by('toonName')
    return queryset
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['Label'] = 'R1-R5'
    return context
  context_object_name = 'toonsCount'

class ToonListViewR6(ListView):
  def get_queryset(self):
    queryset = Toon.objects.filter(relic__gt=6)
    queryset = queryset.values('toonName').annotate(toonNameCount=(Count('toonName'))).order_by('toonName')
    return queryset
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['Label'] = 'R6+'
    return context
  context_object_name = 'toonsCount'

class ToonListView5s(ListView):
  def get_queryset(self):
    queryset = Toon.objects.filter(rarity__gt=5).exclude(combatType='SHIP')
    queryset = queryset.values('toonName').annotate(toonNameCount=(Count('toonName'))).order_by('toonName')
    return queryset
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['Label'] = '5\u2B50+'
    return context
  context_object_name = 'toonsCount'

class ToonListView6s(ListView):
  def get_queryset(self):
    queryset = Toon.objects.filter(rarity__gt=6).exclude(combatType='SHIP')
    queryset = queryset.values('toonName').annotate(toonNameCount=(Count('toonName'))).order_by('toonName')
    return queryset
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['Label'] = '6\u2B50+'
    return context
  context_object_name = 'toonsCount'

class ToonListView7s(ListView):
  def get_queryset(self):
    queryset = Toon.objects.filter(rarity=7).exclude(combatType='SHIP')
    print(queryset.values('toonLevel'))
    queryset = queryset.values('toonName').annotate(toonNameCount=(Count('toonName'))).order_by('toonName')
    return queryset
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['Label'] = '7\u2B50'
    return context
  context_object_name = 'toonsCount'

class ToonListView5sShip(ListView):
  def get_queryset(self):
    queryset = Toon.objects.filter(rarity__gt=5).exclude(combatType='CHARACTER')
    queryset = queryset.values('toonName').annotate(toonNameCount=(Count('toonName'))).order_by('toonName')
    return queryset
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['Label'] = '5\u2B50+'
    return context
  context_object_name = 'toonsCount'

class ToonListView6sShip(ListView):
  def get_queryset(self):
    queryset = Toon.objects.filter(rarity__gt=6).exclude(combatType='CHARACTER')
    queryset = queryset.values('toonName').annotate(toonNameCount=(Count('toonName'))).order_by('toonName')
    return queryset
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['Label'] = '6\u2B50+'
    return context
  context_object_name = 'toonsCount'

class ToonListView7sShip(ListView):
  def get_queryset(self):
    queryset = Toon.objects.filter(rarity=7).exclude(combatType='CHARACTER')
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
    context['toons'] = Toon.objects.filter(player=self.kwargs['pk']).filter(combatType='CHARACTER').order_by('-gp')
    context['ships'] = Toon.objects.filter(player=self.kwargs['pk']).filter(combatType='SHIP').order_by('-gp')
    return context

class ToonDetailView(DetailView):
  model = Toon
  # toons = Toon.objects.filter(player=pk_url_kwarg)
  context_object_name = 'toon'
  slug_field = 'nameKey'
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    # print(self.kwargs)
    context['players'] = Toon.objects.filter(toon=self.kwargs['nameKey']).order_by('nameKey')
    return context
      
def import_data(request):
  import json
  import os
  
  with open('Striker/swgoh/json/config.json') as f:
    config = json.load(f)
    
  from .api_swgoh_help import api_swgoh_help

  allycode = config['allycode']
  client = api_swgoh_help({'username': config['credname'], 'password': config['credpass']})

  def getGuild(api_client, allycode):
      """ :parameters api_swgoh_help instance and player allycode """
      payload = {'allycodes': [allycode], 'language': "eng_us", 'enums': True}
      result = api_client.fetchGuilds(payload)
      return result


  # Fetch a list of guild member allycodes
  members = getGuild(client, allycode)
  with open('Striker/swgoh/json/response.json', 'w') as f:
    json.dump(members, f)
  
  # with open('Striker/swgoh/json/response.json', 'r') as f:
  #   members = json.load(f)
  
  guildResponse = members[0]

  if Guild.objects.filter(pk='1') == False:  
    newGuild = Guild.objects.create(
      guildId = guildResponse['id'],
      name = guildResponse['name'],
      desc = guildResponse['desc'],
      members = guildResponse['members'],
      status = guildResponse['status'],
      required = guildResponse['required'],
      gp = guildResponse['gp'],
      bannerColor = guildResponse['bannerColor'],
      bannerLogo = guildResponse['bannerLogo'],
      message = guildResponse['message']
    )
  else:  
    myGuild = Guild.objects.all().first()
    myGuild.name = guildResponse['name']
    myGuild.desc = guildResponse['desc']
    myGuild.members = guildResponse['members']
    myGuild.status = guildResponse['status']
    myGuild.required = guildResponse['required']
    myGuild.gp = guildResponse['gp']
    myGuild.bannerColor = guildResponse['bannerColor']
    myGuild.bannerLogo = guildResponse['bannerLogo']
    myGuild.message = guildResponse['message']
    myGuild.save()
    print('Guild updated')

  # if myGuild := Guild.objects.get(guildId=guildResponse['id']):
  #   myGuild.name = guildResponse['name']
  #   myGuild.desc = guildResponse['desc']
  #   myGuild.members = guildResponse['members']
  #   myGuild.status = guildResponse['status']
  #   myGuild.required = guildResponse['required']
  #   myGuild.gp = guildResponse['gp']
  #   myGuild.bannerColor = guildResponse['bannerColor']
  #   myGuild.bannerLogo = guildResponse['bannerLogo']
  #   myGuild.message = guildResponse['message']
  #   print('Guild updated')
  # else:
  #   newGuild = Guild.objects.create(
  #     guildId = guildResponse['id'],
  #     name = guildResponse['name'],
  #     desc = guildResponse['desc'],
  #     members = guildResponse['members'],
  #     status = guildResponse['status'],
  #     required = guildResponse['required'],
  #     gp = guildResponse['gp'],
  #     bannerColor = guildResponse['bannerColor'],
  #     bannerLogo = guildResponse['bannerLogo'],
  #     message = guildResponse['message']
  #   )
  #   print('Guild created')
    
  playersResponse = guildResponse['roster']
  
  all_players = Player.objects.all()
  for player in all_players:
    if player not in playersResponse:
      player.active = False
      player.save()
      
  playersList = [player for player in playersResponse]
  guild = Guild.objects.all()[0]
  # for player in playersList:
  #   player.update({"guild": guild})
    
  # [player.update({"guild": guild}) for player in playersList]
  newPlayersObjs = []
  for player in playersList:
    try: 
      oldPlayer = Player.objects.get(playerId = player['id'])
      oldPlayer.name = player['name']
      oldPlayer.allycode = player['allyCode']
      oldPlayer.level = player['level']
      oldPlayer.gp = player['gp']
      oldPlayer.gpChar = player['gpChar']
      oldPlayer.gpShip = player['gpShip']
      oldPlayer.guildMemberLevel = player['guildMemberLevel']
      oldPlayer.active = True
      oldPlayer.save()
      print(oldPlayer.name)
    except:
      newPlayersObjs.append(Player(
        name = player['name'],
        playerId = player['id'],
        allycode = player['allyCode'],
        level = player['level'],
        gp = player['gp'],
        gpChar = player['gpChar'],
        gpShip = player['gpShip'],
        active = True,
        guildMemberLevel = player['guildMemberLevel'],
        guild = guild
      ))

  objs = Player.objects.bulk_create(newPlayersObjs)
  allycodeList = []
  # # allycodeList = [984519997,911364662,885976194,856572921]
  [allycodeList.append(player['allyCode']) for player in playersList]
  print('Requesting rosters for guild members')
  playersResponse = client.fetchPlayers(allycodeList) 
  with open('Striker/swgoh/json/players.json', 'w') as f:
    json.dump(playersResponse, f)
  # with open('Striker/swgoh/json/players.json', 'r') as f:
    # playersResponse = json.load(f)

  Mod.objects.all().delete()
  Skill.objects.all().delete()
  Toon.objects.all().delete()
  ModStat.objects.all().delete()
  Equipped.objects.all().delete()
  ShipCrew.objects.all().delete()
  
  for player in playersResponse:
    playerObj = Player.objects.get(playerId=player['id'])
    print(f'Import for {playerObj.name}')
    toons = player['roster']
    print(toons)
    for toon in toons:
      relic = toon['relic']
 
      if toon['relic']==None or toon['relic']['currentTier']==1:
        relic=0
      else:
        relic=toon['relic']['currentTier']-2
      if toon['primaryUnitStat']==None:
        pus=0
      else:
        pus=toon['primaryUnitStat']
      
      newToonsObj = []

      newToonsObj.append(Toon(
      # Toon.objects.create(
        player = playerObj,
        toonID = toon['id'],
        toonName = toon['defId'],
        nameKey = toon['nameKey'],
        rarity = toon['rarity'],
        toonLevel = toon['level'],
        xp = toon['xp'],
        gp = toon['gp'],
        gearLevel = toon['gear'],
        primaryUnitStat = pus,
        relic = relic,
        combatType = toon['combatType'],
        crew = [i['unitId'] for i in toon['crew']],
        isZeta = [i['isZeta'] for i in toon['skills']],

      ))
      objs = Toon.objects.bulk_create(newToonsObj)
      toonObj = Toon.objects.get(toonID=toon['id'])
      print(f'Added toons for {playerObj.name}')
      
      skills = toon['skills']
      newSkillsObj = []
      for skill in skills:
        newSkillsObj.append(Skill(
          toon = toonObj,  
          skillId = skill['id'],
          tier = skill['tier'],
          nameKey = skill['nameKey'],
          isZeta = skill['isZeta'],
          tiers = skill['tiers']
        ))
      objs = Skill.objects.bulk_create(newSkillsObj)
      print(f'Added skills for {playerObj.name}')
      
      equippeds = toon['equipped']
      newEqippedObj = []
      for equipment in equippeds:
        newEqippedObj.append(Equipped(
          toon = toonObj,
          equipmentId = equipment['equipmentId'],
          slot = equipment['slot'],
          nameKey = equipment['nameKey']
        ))
      objs = Equipped.objects.bulk_create(newEqippedObj)
      print(f'Added gear for {playerObj.name}')
      
      if toon['combatType'] == "SHIP":
        crews = toon['crew']
        newCrewObj = []
        for crew in crews:
          newCrewObj.append(ShipCrew(
            toon = toonObj,
            unitId = crew['unitId'],
            slot = crew['slot'],
            skillId = crew['skillReferenceList'][0]['skillId'],
            requiredTier = crew['skillReferenceList'][0]['requiredTier'],
            requiredRarity = crew['skillReferenceList'][0]['requiredRarity'],
            requiredRelicTier = crew['skillReferenceList'][0]['requiredRelicTier'],
            skillessCrewAbilityId = crew['skilllessCrewAbilityId'],
            gp = crew['gp'],
            cp = crew['cp'],
          ))
        objs = ShipCrew.objects.bulk_create(newCrewObj)
        print(f'Added crew for {playerObj.name}')
      
      mods = toon['mods']
      newModsObj = []
      for mod in mods:
        newModsObj.append(Mod(
          toon = toonObj,
          modId = mod['id'],
          modLevel = mod['level'],
          tier = mod['tier'],
          set = mod['set'],
          pips = mod['pips']
        ))
      objs = Mod.objects.bulk_create(newModsObj)
      print(f'Added mods for {playerObj.name}')
      
      newStatsObj = []
      for mod in mods:
        modObj = Mod.objects.filter(modId=mod['id'])
        modObj = modObj[0]
        ModStat.objects.create(
          mod = modObj,
          statType = 'P',
          unitStat = mod['primaryStat']['unitStat'],
          value = mod['primaryStat']['value']
        )
        sStats = mod['secondaryStat']
        for sStat in sStats:
          newStat = ModStat.objects.create(
            mod = modObj,
            statType = 'S',
            unitStat = sStat['unitStat'],
            roll = sStat['roll'],
            value = sStat['value']
          )
        print(f'Added stats for {playerObj.name}')

  return render(request, 'Striker/import_success.html')