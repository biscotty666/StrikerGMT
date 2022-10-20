from django.contrib import admin

from .models import Guild, Player, Toon, Strike

admin.site.register(Guild)
admin.site.register(Player)
admin.site.register(Toon)
admin.site.register(Strike)
