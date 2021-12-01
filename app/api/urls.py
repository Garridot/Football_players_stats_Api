from django.db import router
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('seasons',views.SeasonsView,basename='seasons') 
router.register('players',views.PlayersView,basename='players') 

app_name = 'api'
urlpatterns = [    
    path('',include(router.urls)),
    path('player_id=<str:player>/',views.MatchesView.as_view())  
]    