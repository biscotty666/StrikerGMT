from django.db import models

class Guild(models.Model):
  guildName = models.CharField(max_length=15)
  description = models.CharField(max_length=100)
  numMembers = models.IntegerField()
  status = models.IntegerField()
  required = models.IntegerField()
  gp = models.IntegerField()
  bannerColor = models.CharField(max_length=25)
  bannerLogo = models.CharField(max_length=25)
  message = models.CharField(max_length=100)

  def __str__(self):
    return f'{self.name} Members: {self.numMembers} GP: {self.gp}'
  
class Player(models.Model):
  playerName = models.CharField(max_length=30)
  playerId = models.CharField(max_length=15)
  allycode = models.IntegerField()
  level = models.IntegerField()
  gp = models.IntegerField()
  gpChar = models.IntegerField()
  gpShip = models.IntegerField()
  active = models.BooleanField(default=True)
  guildMemberLevel = models.IntegerField()
  guildRefId = models.CharField(max_length=30)
  GrandArenaLifeTime = models.IntegerField()
  guild = models.ForeignKey(Guild, on_delete=models.CASCADE)
  
  def __str__(self):
    return f'{self.name}'
  
class Strike(models.Model):
  STRIKE_ACTIVITY = (
    ('TW', 'TW'),
    ('TB', 'TB'),
    ('Tickets', 'Tickets'),
    ('Other', 'Other'),
  )
  player = models.ForeignKey(Player, on_delete=models.CASCADE)
  strike_date = models.DateField()
  ishard = models.BooleanField(default=True)
  comments = models.TextField(max_length=200, blank=True)
  activity = models.CharField(max_length=10, choices=STRIKE_ACTIVITY)
  
  def __str__(self):
    return f'{self.player}, {self.strike_date}, {self.ishard}, {self.activity}, {self.comments}'

class Toon(models.Model):
  player = models.ForeignKey(Player, on_delete=models.CASCADE)
  toonID = models.CharField(max_length=30)
  toonName = models.CharField(max_length=30)
  nameKey = models.CharField(max_length=45)
  rarity = models.IntegerField()
  toonLevel = models.IntegerField()
  gp = models.IntegerField()
  xp = models.IntegerField()
  gearLevel = models.IntegerField()
  primaryUnitStat = models.IntegerField()
  relic = models.IntegerField()
  
  def __str__(self):
    return f'{self.toonName}'

class Gear(models.Model):
  toon = models.ForeignKey(Toon, on_delete=models.CASCADE)
  gearId = models.CharField(max_length=15)
  slot = models.IntegerField()
  nameKey = models.CharField(max_length=15)
  
  def __str__(self):
    return f'{self.gearId} in slot {self.slot}'
  
class Skill(models.Model):
  toon = models.ForeignKey(Toon, on_delete=models.CASCADE)
  skillId = models.CharField(max_length=15)
  tier = models.IntegerField()
  nameKey = models.CharField(max_length=15)
  isZeta = models.BooleanField(default=False)
  tiers = models.IntegerField()
  
  def __str__(self):
    return f'{self.skillId}: {self.tier} of {self.tiers}'
  

class Mod(models.Model):
  toon = models.ForeignKey(Toon, on_delete=models.CASCADE)
  modId = models.CharField(max_length=15)  
  modLevel = models.IntegerField()
  tier = models.IntegerField()
  slot = models.IntegerField()
  set = models.IntegerField()
  pips = models.IntegerField()
  
class Mod_Stat(models.Model):
  mod = models.ForeignKey(Mod, on_delete=models.CASCADE)
  modID = models.CharField(max_length=15)
  unitStat = models.IntegerField()
  value = models.IntegerField()
  roll = models.IntegerField()
  statType = models.CharField(max_length=15)

