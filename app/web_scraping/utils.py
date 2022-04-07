from datetime import datetime
from database.models import *

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


def clean_data(df):    

    df.columns = range(df.shape[1])

    dates = [] 
    for d in df[1]:

        date = f"{d[3:5]} {d[5:]}".strip() 
        date = datetime.strptime(date,'%d %b %Y').date()      
        dates.append(date)    

    df.insert(1, "Date", dates, allow_duplicates=False) 

    #Delete unnecessary colums 
    df = df.drop([1,2, 7,8 ,9,], axis=1) 

    # Rename colums
    df = df.rename({0:'Competition', 3:'Home_team', 4:'Result', 5:'Away_team', 6:'Goals',},axis=1) 
    
    df.fillna(0)
    
    return df


def check_season(soup):
    # get or create the season

        title = soup.find('h2').text.strip()
        season = f"{title[-9:]}" 
        qs_season  = Seasons.objects.get_or_create(season=season) 
        return season[0]


def check_player(soup,url): 

    # get or create the player

        player = soup.find('tr',class_='first').find('td').text.strip()  

        if  Players.objects.filter(name=player).filter():
            return qs_player 

        else:  
            create_player(soup,url)                     
            qs_player  = Players.objects.get(name=player) 

        return player         


def create_player(soup,url):
    player_data  = soup.find('div',class_='twoSoccerColumns clearfix')
    data = player_data.findAll('strong')
    data = [i.text.split() for i in data]
    
    
    club          = try_data_player.club(soup)
    name          = try_data_player.name(data)
    height        = try_data_player.height(data)
    age           = try_data_player.age(data)
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




def check_the_last_match(soup,player,qs_season,df):
        

    matches = soup.findAll('tr',class_='match')                     
    tr    = [a.text.split() for a in matches]

    data  = tr[-1] 
    date  = f"{data[2][:2]} {data[2][2:]} {data[3][:4]}"
    date  = datetime.strptime(date,'%d %b %Y').date()

    match = Matches.objects.filter(player=player,season=qs_season.id,date=date)

    if match == None:
        return None