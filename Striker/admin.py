from django.contrib import admin
from .models import Guild, Player, Strike, Toon, Skill, Mod, Equipped, ModStat, ShipCrew 
from rest_framework.authtoken.admin import TokenAdmin

TokenAdmin.raw_id_fields = ['user']
admin.site.register(Guild)
admin.site.register(Player)
admin.site.register(Strike)
admin.site.register(Toon)
admin.site.register(Skill)
admin.site.register(Mod)
admin.site.register(Equipped)
admin.site.register(ModStat)
admin.site.register(ShipCrew)