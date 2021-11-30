# rest_framework
from rest_framework.response import Response
from rest_framework import  generics
from rest_framework.permissions import *
from rest_framework.authentication import TokenAuthentication 
from rest_framework.viewsets import *
 
# django_q
from django_q.tasks import schedule
from django_q.models import Schedule


from web_scraping.views import *
from database.models import *

from django.shortcuts import get_object_or_404
from .serializers import *




class BaseViewSet(ModelViewSet):
    
    authentication_class   = (TokenAuthentication,)
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]

        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated]   

        else:
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

    serializer_class = MatchesSerializer
    permissions      = (IsAuthenticated)
    model            = Matches
    
    def get_queryset(self): 
        player = self.kwargs['player']        
        return Matches.objects.filter(player=player,).all() 
    
    
try:
    if Schedule.objects.filter(name="CheckMatchToday").delete():
        schedule(name='CheckMatchToday',func="web_scraping.views.UpdateStast",schedule_type=Schedule.MINUTES,)
except:                
    schedule(name='CheckMatchToday',func="web_scraping.views.UpdateStast",schedule_type=Schedule.MINUTES,) 
