from django.db import models

class Guild(models.Model):
  guildName = models.CharField(max_length=15)
  description = models.CharField(max_length=100)
  numMembers = models.IntegerField()
  status = models.IntegerField(null=True)
  required = models.IntegerField(null=True)
  gp = models.IntegerField()
  bannerColor = models.CharField(max_length=25, blank=True)
  bannerLogo = models.CharField(max_length=25, blank=True)
  message = models.CharField(max_length=100, blank=True)

  def __str__(self):
    return f'{self.guildName} Members: {self.numMembers} GP: {self.gp}'
  
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
    return f'{self.playerName}, GP: {self.gp}'
  
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


