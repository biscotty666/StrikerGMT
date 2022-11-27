from django.db import models

class Guild(models.Model):
  guildId = models.CharField(max_length=20,blank=True)
  name = models.CharField(max_length=15,blank=True)
  desc = models.CharField(max_length=100,blank=True)
  members = models.IntegerField()
  status = models.IntegerField(null=True)
  required = models.IntegerField(null=True)
  gp = models.IntegerField()
  bannerColor = models.CharField(max_length=25, blank=True)
  bannerLogo = models.CharField(max_length=25, blank=True)
  message = models.CharField(max_length=100, blank=True)

  def __str__(self):
    return f'{self.name} Members: {self.members} GP: {self.gp}'
  
class Player(models.Model):
  name = models.CharField(max_length=30)
  playerId = models.CharField(max_length=15)
  allycode = models.IntegerField()
  level = models.IntegerField()
  gp = models.IntegerField()
  gpChar = models.IntegerField()
  gpShip = models.IntegerField()
  active = models.BooleanField(default=True)
  guildMemberLevel = models.CharField(max_length=20, blank=True)
  updated = models.CharField(max_length=30,blank=True)
  guild = models.ForeignKey(Guild, default=1, on_delete=models.CASCADE)

  class Meta:
    ordering = ['playerId']
  
  def __str__(self):
    return f'{self.name}, playerId:{self.playerId}, GP: {self.gp}'
  
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
  
  
  
  class Meta:
    ordering = ["-strike_date"]
  
  def __str__(self):
    return f'{self.pk}, {self.player}, {self.strike_date}, {self.ishard}, {self.activity}, {self.comments}'

class Toon(models.Model):
  player = models.ForeignKey(Player, on_delete=models.CASCADE)
  toonID = models.CharField(max_length=45)
  toonName = models.CharField(max_length=45)
  nameKey = models.CharField(max_length=45)
  rarity = models.IntegerField()
  toonLevel = models.IntegerField()
  xp = models.IntegerField(default=0)
  gp = models.IntegerField()
  gearLevel = models.IntegerField()
  primaryUnitStat = models.IntegerField()
  relic = models.IntegerField()
  combatType = models.CharField(max_length=30, blank=True)
  crew = models.CharField(max_length=45, blank=True)
  isZeta = models.CharField(max_length=45, blank=True)
  forceAlignment = models.CharField(max_length=45, blank=True)
  def __str__(self):
    return f'{self.toonName}'
  
class Mod(models.Model):
  toon = models.ForeignKey(Toon, on_delete=models.CASCADE)
  modId = models.CharField(max_length=30)
  modLevel = models.SmallIntegerField()
  tier = models.SmallIntegerField()
  set = models.SmallIntegerField()
  pips = models.SmallIntegerField()
  
  def __str__(self):
    return f'{self.modId}, {self.modLevel}, {self.tier}, {self.set}, {self.pips}'
  
class ModStat(models.Model):
  mod = models.ForeignKey(Mod, on_delete=models.CASCADE)
  statType = models.CharField(max_length=1, default='P')
  unitStat = models.CharField(max_length=30, default='')
  value = models.DecimalField(max_digits=10, decimal_places=5)
  roll = models.SmallIntegerField(default=0)
  
  def __str__(self):
    return f'{self.statType}, {self.unitStat}, {self.value}, {self.roll}'
  
class Skill(models.Model):
  toon = models.ForeignKey(Toon, on_delete=models.CASCADE)
  skillId = models.CharField(max_length=30)
  tier = models.SmallIntegerField()
  nameKey = models.CharField(max_length=30)
  isZeta = models.BooleanField(default=False)
  tiers = models.SmallIntegerField()

  def __str__(self):
    return f'Skill: {self.skillId}, Tier: {self.tier}, Skill Name: {self.nameKey}, Zeta: {self.isZeta}'

class Equipped(models.Model):
  toon = models.ForeignKey(Toon, on_delete=models.CASCADE)
  equipmentId = models.CharField(max_length=6, blank=True)
  slot = models.SmallIntegerField(blank=True)
  nameKey = models.CharField(max_length=35, blank=True) 
  
  def __str__(self):
    return f'Gear: {self.nameKey}' 
 
class ShipCrew(models.Model):
  toon = models.ForeignKey(Toon, on_delete=models.CASCADE)
  unitId = models.CharField(max_length=40, blank=True) 
  skillId = models.CharField(max_length=40, blank=True) 
  skillessCrewAbilityId = models.CharField(max_length=35, blank=True) 
  slot = models.SmallIntegerField(blank=True)
  requiredTier = models.SmallIntegerField(blank=True)
  requiredRarity = models.SmallIntegerField(blank=True)
  requiredRelicTier = models.SmallIntegerField(blank=True)
  gp = models.SmallIntegerField(blank=True)
  cp = models.DecimalField(max_digits=10, decimal_places=5)
  
  def __str__(self):
    return f'Crew: {self.unitId}, GP: {self.gp}, CP: {self.cp}'


