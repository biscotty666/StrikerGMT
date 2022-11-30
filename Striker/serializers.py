from .models import Player, Strike, Toon, Mod, Skill, ModStat, Equipped
from rest_framework import serializers

class PlayerSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Player
    fields = ['id','name', 'gp', 'gpChar', 'gpShip', 'allycode', 'level']
    
class StrikeSerializer(serializers.HyperlinkedModelSerializer):
  strike_date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d','%m/%d/%y'])
  class Meta:
    model = Strike
    fields = ['id','player', 'strike_date', 'activity', 'ishard', 'comments']
    
class ToonSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Toon
    fields = ['id','player', 'toonID', 'nameKey', 'toonName',
              'rarity', 'toonLevel', 'xp', 'gp', 'gearLevel',
              'primaryUnitStat', 'relic']
    