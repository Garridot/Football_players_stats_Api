from django.contrib import admin
from .models import *

# Register your models here.

class PlayersAdmin(admin.ModelAdmin):
    list_display  = ('id','name','age','nationality','height')    
    search_fields = ('name',)

class MatchesAdmin(admin.ModelAdmin):
    list_display  = ('id','player','season','date','competition','home_team','result','away_team','goals')
    list_filter   = ('player','season')
    search_fields = ('player','season')

class SeasonsAdmin(admin.ModelAdmin):
    list_display  = ('id','season')

admin.site.register(Players,PlayersAdmin)
admin.site.register(Seasons,SeasonsAdmin)
admin.site.register(Matches,MatchesAdmin)