# rest_framework
from django.db.models.base import ModelBase
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import  generics
from rest_framework.permissions import *
from rest_framework.authentication import TokenAuthentication 
from rest_framework.viewsets import *
from rest_framework import status

# django_q
from django_q.tasks import schedule
from django_q.models import Schedule

# django
from web_scraping.views import *
from database.models import *
from django.shortcuts import get_object_or_404
from .serializers import *
from django.views.generic import TemplateView


class MainView(TemplateView):
    template_name = "main_page.html"



class BaseViewSet(ModelViewSet):

    authentication_class = (TokenAuthentication,)    
    
    def get_permissions(self):
        permission_classes = [IsAuthenticated,] 
        
        if self.action == 'create':
            permission_classes = [IsAuthenticated,IsAdminUser]

        elif self.action == 'update': 
            permission_classes = [IsAuthenticated,IsAdminUser]

        elif self.action == 'partial_update':
            permission_classes = [IsAuthenticated,IsAdminUser]

        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated,IsAdminUser]

        return [permission() for permission in permission_classes]
        
        

        

    

class PlayersView(BaseViewSet): 
    
    serializer_class = PlayersSerializer
    queryset         = Players.objects.all()

    def list(self, request):
        queryset   = Players.objects.all()
        serializer = PlayersSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset   = Players.objects.all()
        qs         = get_object_or_404(queryset, pk=pk)
        serializer = PlayersSerializer(qs)
        return Response(serializer.data)
   
class SeasonsView(BaseViewSet): 

    serializer_class = SeasonsSerializer
    queryset         = Seasons.objects.all()
    
    def list(self, request):
        queryset   = Seasons.objects.all()
        serializer = SeasonsSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset   = Seasons.objects.all()
        qs         = get_object_or_404(queryset, pk=pk)
        serializer = SeasonsSerializer(qs)
        return Response(serializer.data)
 
class MatchesView(generics.ListAPIView):

    serializer_class    = MatchesSerializer
    permission_classes = [IsAuthenticated,] 
    authentication_class = (TokenAuthentication,)
    
    def get_queryset(self):

        queryset  = Matches.objects.all()
        player    = self.kwargs['player']
        season    = self.request.query_params.get('season')

        if season is not None:
            queryset  = queryset.filter(player=player,season=season)
            if queryset.exists():
                return queryset
            else:  
                if Players.objects.filter(id=player) and Seasons.objects.filter(id=season):
                    raise serializers.ValidationError(
                        {"detail": f"{Players.objects.get(id=player)} has not played any matches in {Seasons.objects.get(id=season)}",
                        'code':status.HTTP_404_NOT_FOUND}
                    )
                else:
                    raise serializers.ValidationError({"detail": "player or season doesn't exist",'code':status.HTTP_400_BAD_REQUEST})
        else:      
            return queryset.filter(player=player)  
    
try:
    if Schedule.objects.filter(name="CheckMatchToday").delete():
        schedule(name='CheckMatchToday',func="web_scraping.views.UpdateStast",schedule_type=Schedule.MINUTES,)
except:                
    schedule(name='CheckMatchToday',func="web_scraping.views.UpdateStast",schedule_type=Schedule.MINUTES,) 
