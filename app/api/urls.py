from django.db import router
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('seasons',views.SeasonsView,basename='seasons') 
router.register('players',views.PlayersView,basename='players') 

app_name = 'api'
urlpatterns = [    
    path('',views.MainView.as_view()),
    path('api/',include(router.urls)),
    path('api/matches/player=<str:player>/',views.MatchesView.as_view())  
]    