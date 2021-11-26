from bs4 import BeautifulSoup
from django.http.response import HttpResponse
import requests
import pandas 
import sqlite3
import psycopg2
from datetime import datetime
from database.models import *
from app.settings import DATABASES 

print(DATABASES['default']['NAME'])

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

                    url = f'https://www.soccerbase.com/players/player.sd?player_id={p.player_id}' 
                    response = requests.get(url)
                    soup  = BeautifulSoup(response.text, 'html.parser')

                    title = soup.find('h2').text.strip()
                    table = soup.findAll('tr',class_='match')    
                    tr    = [a.text.split() for a in table]            
                    data  = tr[-1]    
                    
                    date  = f"{data[2][:2]} {data[2][2:]} {data[3][:4]}" 
                    date  = datetime.strptime(date,'%d %b %Y').date() 



                    match = Matches.objects.filter(player_id=p).last()

                    if date != match.date:
                        competition = f"{data[0]} {data[1][:-2]}"
                        home_team   = f"{data[3][4:-1]}"
                        away_team   = f"{data[5][1:]}"
                        goals       = f"{data[6][-1]}"
                        
                        try:
                            goals = int(goals)
                            goals = f"{goals}"
                        except:
                            goals = '0'   

                        result      = f"{data[3][-1:]} {data[4]} {data[5][0]}"                        
                        season      = Seasons.objects.get(season = f"{title[-9:]}") 

                        conn   = psycopg2.connect('db.d2fcrdpv7dt8bs')    
                        cursor = conn.cursor()        
                        try:
                            index_player = Matches.objects.last().id 
                            if index_player:     
                                index  = int(index_player) + 1
                                index  = index 
                        except:
                            index = 1 

                        cursor.execute('''
                            INSERT INTO database_matches VALUES (?,?,?,?,?,?,?,?,?)''',
                            (index,date,competition,home_team,result,away_team,goals,p.id,season.id))    
                        conn.commit()
                        conn.close()
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
    
    id = url[55:]
    Players.objects.create(name=name,age=age,height=height,nationality=nationality,club=club,date_of_birth=date_of_birth,player_id=id)

def CleanData(df,qs_player,qs_season): 
        
    df.columns = range(df.shape[1])
    
    df.drop(index=df.index[0], 
        axis=0, 
        inplace=True)
    
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
    conn   = psycopg2.connect('db.d2fcrdpv7dt8bs')    
    cursor = conn.cursor()
    
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
        try:
            match = Matches.objects.get(player=player,season=season,date=row.Date)   
            if match:
                break
        except:        
            goals = int(row.Goals)     
            cursor.execute('''
            INSERT INTO database_matches VALUES (?,?,?,?,?,?,?,?,?)''',
            (index,row.Date,row.Competition,row.Home_team,row.Result,row.Away_team,goals,player,season))
            
            index += 1

    conn.commit()
    conn.close()
    return HttpResponse(f'{qs_player.name}, {qs_season.season} stats added successufully')
  



 