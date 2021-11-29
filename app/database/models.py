from django.db import models

# Create your models here.

class Players(models.Model):
    name           =  models.CharField(max_length=100)
    age            =  models.CharField(max_length=100)
    date_of_birth  =  models.DateField()
    nationality    =  models.CharField(max_length=100)
    club           =  models.CharField(max_length=100)
    height         =  models.CharField(max_length=100)
    player_id      =  models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name        = 'Player'
        verbose_name_plural = 'Players'    

class Seasons(models.Model):
    season         =  models.CharField(max_length=100)

    def __str__(self):
        return self.season  

    class Meta():
        verbose_name        = 'Season'
        verbose_name_plural = 'Seasons'      

class Matches(models.Model):
    
    player         =  models.ForeignKey(Players,on_delete=models.CASCADE)
    season         =  models.ForeignKey(Seasons,on_delete=models.CASCADE)
    date           =  models.DateField()
    competition    =  models.CharField(max_length=100)
    home_team      =  models.CharField(max_length=100)
    result         =  models.CharField(max_length=100)
    away_team      =  models.CharField(max_length=100)     
    goals          =  models.CharField(max_length=2)

    class Meta():
        verbose_name        = 'Match'
        verbose_name_plural = 'Matches'