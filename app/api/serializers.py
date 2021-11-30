from rest_framework import serializers
from database.models import *

class PlayersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Players
        fields =  ("id", "name", "age", "date_of_birth", "nationality",  "club", "height")
        

class SeasonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seasons
        fields =  ('__all__')


class MatchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matches
        fields =  ('__all__')                
