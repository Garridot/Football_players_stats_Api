from rest_framework import serializers
from database.models import *

class PlayersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Players
        fields =  ('__all__')


class SeasonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seasons
        fields =  ('__all__')


class MatchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matches
        fields =  ('__all__')                

class ScrapingSerializer(serializers.Serializer):
    url = serializers.URLField()