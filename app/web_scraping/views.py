from bs4 import BeautifulSoup
from django.http.response import HttpResponse
import requests
import pandas 
import sqlite3
from datetime import datetime
from database.models import *
import psycopg2
from app.settings import DATABASES


def UpdateStast():  
       
    url = 'https://www.soccerbase.com/matches/home.sd'    
    response = requests.get(url)
    
    soup   = BeautifulSoup(response.text, 'html.parser')      
    matches = soup.find('table',class_='soccerGrid homeMatchGrid')    

    df = pandas.read_html(str(matches))
    df = df[0]
    df = df[df[1].str.contains('ft',case=False)]
    df = df
    df.columns = range(df.shape[1])
    df = df.drop([0,2,6,7,8,9,10,11], axis=1)

    if df.shape[0] == 0:

        print('No math found.')

    else:
        print(df)
        home_team = df[3]
        away_team = df[5]
        teams = []        
        for h,a in zip(home_team,away_team):
            teams.append(h)
            teams.append(a)
        
        for p in Players.objects.all():  
            
            for t in teams:
                
                if t == p.club or t == p.nationality: 
                    print(p)
                    url = f'https://www.soccerbase.com/players/player.sd?player_id={p.player_id}' 
                    response = requests.get(url)
                    soup  = BeautifulSoup(response.text, 'html.parser')

                    title = soup.find('h2').text.strip()
                    table = soup.findAll('tr',class_='match')    
                    tr    = [a.text.split() for a in table]            
                    data  = tr[-1]    
                    
                    date  = f"{data[2][:2]} {data[2][2:]} {data[3][:4]}"
                    
                    date  = datetime.strptime(date,'%d %b %Y').date() 
                    
                    match = Matches.objects.filter(player=p).last()  
                               
                    if date != match.date:
                        competition = f"{data[0]} {data[1][:-2]}"
                        home_team   = f"{data[3][4:-1]}"
                        away_team   = f"{data[5][1:]}"
                        
                        
                        
                        try:
                            goals       = f"{data[6][-1]}"
                            goals = int(goals)
                            goals = f"{goals}"
                        except:
                            goals = '0'   

                        result      = f"{data[3][-1:]} {data[4]} {data[5][0]}"                        
                        season      = Seasons.objects.get(season = f"{title[-9:]}") 

                        
                        Matches.objects.create(
                        date        = date,
                        competition = competition,
                        home_team   = home_team,
                        result      = result,
                        away_team   = away_team,
                        goals       = goals,
                        player      = Players.objects.get(id=p.id),
                        season      = Seasons.objects.get(id=season.id)
                        )  
                        print('Stat Added')         
                    else:
                        return None 
                else:                   
                    None        

    
def addPlayerStast(url):
    response = requests.get(url)
    soup   = BeautifulSoup(response.text, 'html.parser')
        
    title = soup.find('h2').text.strip()
    table = soup.find('table',class_='soccerGrid listWithCards')
    df = pandas.read_html(str(table))

    df = df[0]


    season = f"{title[-9:]}"    
    try:
        qs_season  = Seasons.objects.get(season=season)
        if qs_season:
            qs_season  = qs_season
    
    except:              
        qs_season  = Seasons.objects.create(season=season)
        qs_season  = Seasons.objects.get(season=season)
    
    player = soup.find('tr',class_='first').find('td').text.strip()
    
    try:
        qs_player  = Players.objects.get(name=player)
        if qs_player:
            qs_player  = qs_player
    
    except: 
        
        CreatePlayer(soup,url)                     
        qs_player  = Players.objects.get(name=player) 
   
    
    CleanData(df,qs_player,qs_season)


def CreatePlayer(soup,url):
    player_data  = soup.find('div',class_='twoSoccerColumns clearfix')
    data = player_data.findAll('strong')
    data = [i.text.split() for i in data]
    
    ##### Clean Data

    club   = soup.find('table',class_='table right career').find('td',class_='first left bull').text.strip() 

    try:
        name = f"{data[0][0]} {data[0][1]}"
    except:
        name = f"{data[0][0]}"    
    
    try:
        try:
            height = f"{data[2][2]}".replace('(',"").replace(")","")
        except: 
            height = f"{data[2][1]}".replace('(',"").replace(")","") 
    except:
        height = 'No Data'

    age  = data[1][0]

    nationality   = data[5][0]

    date_of_birth = soup.find('table',class_='clubInfo').findAll('td')
    date_of_birth = [i.text.split() for i in date_of_birth]
    date_of_birth = f"{date_of_birth[1][2]} {date_of_birth[1][3]} {date_of_birth[1][4]}".replace('(',"").replace(")","")
    date_of_birth = datetime.strptime(date_of_birth,'%d %b, %Y').date()  
    
    
    id = url[55:60]
    
    Players.objects.create(name=name,age=age,height=height,nationality=nationality,club=club,date_of_birth=date_of_birth,player_id=id)


def CleanData(df,qs_player,qs_season): 
        
    df.columns = range(df.shape[1])
    
    dates = [] 
    for d in df[1]:
        d = f"{d[3:5]} {d[5:]}" 
        d = d.strip()         
        d = datetime.strptime(d,'%d %b %Y').date()      
        dates.append(d)

    # Create Date colum 
    
    df.insert(1, "Date", dates, allow_duplicates=False) 

    # Delete unnecessary colums    
    
    df = df.drop([1,2, 7,8 ,9,], axis=1) 

    # Rename colums                
    
    df = df.rename({0:'Competition', 3:'Home_team',
    4:'Result', 5:'Away_team', 6:'Goals',},axis=1) 
       
    df = df.fillna(0)
    
    SaveData(df,qs_player,qs_season)


def SaveData(df,qs_player,qs_season):        
     
    try:
        index_player = Matches.objects.last().id 
        if index_player:     
            index  = int(index_player) + 1
            index  = index 
    except:
        index = 1        

    
    player = int(qs_player.id)
    season = int(qs_season.id)

    

    for row in df.itertuples(): 
        
        match = Matches.objects.filter(player=player,season=season,date=row.Date)   
        if match.exists():
            None
        else:    
            goals = int(row.Goals)   

            Matches.objects.create(
                date        = row.Date,
                competition = row.Competition,
                home_team   = row.Home_team,
                result      = row.Result,
                away_team   = row.Away_team,
                goals       = goals,
                player      = Players.objects.get(id=player),
                season      = Seasons.objects.get(id=season)
                )  
             
    return HttpResponse(f'{qs_player.name}, {qs_season.season} stats added successufully')

# url = 'https://www.soccerbase.com/players/player.sd?player_id=39850'
# addPlayerStast(url)

UpdateStast()