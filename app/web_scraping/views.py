from bs4 import BeautifulSoup
from django.http.response import HttpResponse
import requests
import pandas 
from datetime import datetime
from database.models import *



import os

class get_season():

    def season(soup):
        title = soup.find('h2').text.strip()
        season = f"{title[-9:]}" 
        qs_season  = Seasons.objects.get_or_create(season=season) 
        return qs_season[0]

class get_player():

    def player(soup,url): 
        player = soup.find('tr',class_='first').find('td').text.strip()        
        try:
            qs_player  = Players.objects.get(name=player)               
        except:             
            CreatePlayer.create(soup,url)                     
            qs_player  = Players.objects.get(name=player) 

        return qs_player       

class try_data_player():

    def name(data):
        try:
            name = f"{data[0][0]} {data[0][1]}"
        except:
            name = f"{data[0][0]}"
        return name 


    def club(soup):
        club   = soup.find('table',class_='table right career').find('td',class_='first left bull').text.strip()   
        return club  


    def age(data):
        age  = data[1][0]
        return age 


    def nationality(data):
        nationality   = data[5][0]
        return nationality   


    def height(data):
        try:
            try:
                height = f"{data[2][2]}".replace('(',"").replace(")","")
            except: 
                height = f"{data[2][1]}".replace('(',"").replace(")","") 
        except:
            height = 'No Data'
        return height  


    def date_of_birth(soup): 
        date_of_birth = soup.find('table',class_='clubInfo').findAll('td')
        date_of_birth = [i.text.split() for i in date_of_birth]
        date_of_birth = f"{date_of_birth[1][2]} {date_of_birth[1][3]} {date_of_birth[1][4]}".replace('(',"").replace(")","")
        date_of_birth = datetime.strptime(date_of_birth,'%d %b, %Y').date() 
        return date_of_birth     

class check_the_last_match():
    def check(soup,player,qs_season,df):
           

        matches = soup.findAll('tr',class_='match')                     
        tr    = [a.text.split() for a in matches]

        data  = tr[-1] 
        date  = f"{data[2][:2]} {data[2][2:]} {data[3][:4]}"
        date  = datetime.strptime(date,'%d %b %Y').date()

        match = Matches.objects.filter(player=player,season=qs_season.id,date=date)

        if match == None:
            return None
            


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
        teams     = [] 

        for h,a in zip(home_team,away_team):
            teams.append(h)
            teams.append(a)
        
        for player in Players.objects.all(): 

            scrap = Scraping.objects.get(player=player)

            for team in teams:
                
                if team == player.club or team == player.nationality: 

                    url = f'https://www.soccerbase.com/players/player.sd?player_id={scrap.id_to_scraping}' 
                    response = requests.get(url)
                    soup  = BeautifulSoup(response.text, 'html.parser')
                    table = soup.find('table',class_='soccerGrid listWithCards') 
                    
                    df = pandas.read_html(str(table))
                    df = df[0]  

                    qs_season = get_season.season(soup)
                    
                    match = check_the_last_match.check(soup,player,qs_season,df)

                                         

                    if match == None:
                        df = CleanData.clean(df)
                        SaveData.save(df,qs_player=player,qs_season=qs_season) 
                    
                else:                   
                    None        

    
def CreateStast(url):
    response = requests.get(url)
    soup   = BeautifulSoup(response.text, 'html.parser')
        
    
    table = soup.find('table',class_='soccerGrid listWithCards')
    df = pandas.read_html(str(table))

    df = df[0]    
    qs_season  = get_season.season(soup)
    qs_player = get_player.player(soup,url) 
    
    df = CleanData.clean(df)
    return SaveData.save(df,qs_player,qs_season)


class CreatePlayer():

    def create(soup,url):        
        player_data  = soup.find('div',class_='twoSoccerColumns clearfix')
        data = player_data.findAll('strong')
        data = [i.text.split() for i in data]
        
        
        club   = try_data_player.club(soup)
        name   = try_data_player.name(data)
        height = try_data_player.height(data)
        age    = try_data_player.age(data)
        nationality   = try_data_player.nationality(data)
        date_of_birth = try_data_player.date_of_birth(soup)


        
        player = Players.objects.create(
            name          = name,
            age           = age,
            height        = height,
            nationality   = nationality,        
            club          = club,
            date_of_birth = date_of_birth)

        player_id = url[55:60]
        Scraping.objects.create(player=player,id_to_scraping=player_id)


class CleanData():

    def clean(df):         
        df.columns = range(df.shape[1])
        
        # Create Date colum 
        dates = [] 
        for d in df[1]:
            d = f"{d[3:5]} {d[5:]}" 
            d = d.strip()         
            d = datetime.strptime(d,'%d %b %Y').date()      
            dates.append(d)    
        df.insert(1, "Date", dates, allow_duplicates=False) 

        # Delete unnecessary colums    
        
        df = df.drop([1,2, 7,8 ,9,], axis=1) 

        # Rename colums                
        
        df = df.rename({0:'Competition', 3:'Home_team',
        4:'Result', 5:'Away_team', 6:'Goals',},axis=1) 
        
        df = df.fillna(0)
        
        return df


class SaveData():
    def save(df,qs_player,qs_season):      
         
        player = qs_player.id        
        season = qs_season.id

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
                
        print(f'{Players.objects.get(id=player)}, {Seasons.objects.get(id=season)} stats added successufully')



# class Selenium():
#     from selenium import webdriver
#     from selenium.webdriver.chrome.service import Service

#     web_site = 'https://www.soccerbase.com/players/player.sd?player_id=44554'
    

#     s = Service( '/Users/Garrido/Desktop/chromedriver')

#     options = webdriver.ChromeOptions() 
#     options.add_argument('--headless') 
#     options.add_argument('--log-level=1')
#     driver = webdriver.Chrome(service=s,options = options)

    
#     driver.get(web_site)

#     select = driver.find_element_by_id('seasonSelect')

#     options = [x for x in select.find_elements_by_tag_name("option")]

#     for element in options:    
#         season_id = int(element.get_attribute("value"))
#         if season_id != 0:
#             url = f'{web_site}&season_id={season_id}'    
#             CreateStast(url)  


