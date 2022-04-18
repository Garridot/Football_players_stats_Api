from ast import Break
from bs4 import BeautifulSoup
import requests
import pandas 
from database.models import *

from .utils import *

import os
            

def UpdateStast():     

    response = requests.get('https://www.soccerbase.com/matches/home.sd' )     
    
    soup     = BeautifulSoup(response.text, 'html.parser')      
    matches  = soup.find('table',class_='soccerGrid homeMatchGrid')      

    df = pandas.read_html(str(matches))
    df = df[0]

    # Fiilter if the match is finished  
    df = df[df[1].str.contains('ft',case=False)]    
    df = df  

    df.columns = range(df.shape[1])
    df = df.drop([0,2,6,7,8,9,10,11], axis=1)    

    if_matches_found(df)


def if_matches_found(df):

    if len(df) == 0: print('No math found.')

    else:
        print(df)
        
        home_team = df[3]
        away_team = df[5]
        teams     = [] 

        for h,a in zip(home_team,away_team):
            teams.append(h)
            teams.append(a)

        players = []       

        for team in teams:
            
            fil1 = Players.objects.filter(club=team)
            fil2 = Players.objects.filter(nationality=team)
            
            [players.append(i) for i in fil1 if fil1]
            [players.append(i) for i in fil2 if fil2]

    if not players: Break
    else: update_player_stats(players)            


def update_player_stats(players):

    for player in players: 

            scrap = Scraping.objects.get(player=player)

            url = f'https://www.soccerbase.com/players/player.sd?player_id={scrap.id_to_scraping}' 
            response = requests.get(url)
            soup  = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table',class_='soccerGrid listWithCards') 
            
            df = pandas.read_html(str(table))
            df = df[0]  

            qs_season = check_season(soup)
            
            match = check_the_last_match(soup,player,qs_season,df)

                                         

            if match == None:
                df = clean_data(df)
                save_data(df,player=player,season=qs_season) 

      

class CreateStast:

    def get_stats(url):

        response = requests.get(url)
        soup     = BeautifulSoup(response.text, 'html.parser')    
        table    = soup.find('table',class_='soccerGrid listWithCards')

        df = pandas.read_html(str(table))
        df = df[0] 
        df = clean_data(df)        

        season  = check_season(soup)
        player  = check_player(soup,url) 

        return save_data(df,player,season)



def save_data(df,player,season):

    player = player.id        
    season = Seasons.objects.get(season=season)

    for row in df.itertuples(): 
        
        match = Matches.objects.filter(player=player,season=season.id,date=row.Date)   
        if match.exists():
            print(f'{player},{row.Date} already exists.')
        else: 

            try:goals = int(row.Goals) 
            except:goals = 0  

            Matches.objects.create(
                date        = row.Date,
                competition = row.Competition,
                home_team   = row.Home_team,
                result      = row.Result,
                away_team   = row.Away_team,
                goals       = goals,
                player      = Players.objects.get(id=player),
                season      = season
                )  

            return print(f'{player}, {row.Date} stats added successufully'  )





























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


