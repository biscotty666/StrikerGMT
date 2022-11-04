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
  guildMemberLevel = models.IntegerField()
  updated = models.CharField(max_length=30,blank=True)
  guild = models.ForeignKey(Guild, default=1, on_delete=models.CASCADE)
  
  def __str__(self):
    return f'{self.name}, GP: {self.gp}'
  
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
    return f'{self.player}, {self.strike_date}, {self.ishard}, {self.activity}, {self.comments}'

class Toon(models.Model):
  player = models.ForeignKey(Player, on_delete=models.CASCADE)
  toonID = models.CharField(max_length=45)
  toonName = models.CharField(max_length=45)
  nameKey = models.CharField(max_length=45)
  rarity = models.IntegerField()
  toonLevel = models.IntegerField()
  gp = models.IntegerField()
  gearLevel = models.IntegerField()
  primaryUnitStat = models.IntegerField()
  relic = models.IntegerField()
  
  def __str__(self):
    return f'{self.toonName}'
  

