from django.db import router
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('seasons',views.SeasonsView,basename='seasons') 
router.register('players',views.PlayersView,basename='players') 
router.register('matches',views.MatchesView,basename='matches') 

app_name = 'main'
urlpatterns = [    
    path('',include(router.urls)),  
]    