# Players Stats API
Players Stats API is an api that saves statistics of football players. The api scrapes their data using asynchronous tasks. The data is updated every minute. Users will be able to access the data via a token.

## Information

This is a consumption-only API — only the HTTP GET method is available on resources.

### What is an API?

An API (Application Programming Interface) is a contract that allow developers to interact with an application through a set of interfaces. In this case, the application is a database of thousands of Pokémon-related objects, and the interfaces are URL links. A RESTful API is an API that conforms to a set of loose conventions based on HTTP verbs, errors, and hyperlinks.



## What information is stored here?



### Player
* Id
* Name
* Age
* Date of birth
* Nationality
* Club
* Height
### Season
* Id
* Season
### Match
* Id
* Player
* Season
* Date
* Competition
* Home team
* Result
* Away team
* Goals

## Endpoints

Base URL for all endpoints https://football-players-stats-api.herokuapp.com

GET /api/players/

* GET /api/players/{player_id}/
* GET /api/seasons/
* GET /api/seasons/{season_id}
* GET /api/matches/player={player_id}
* GET /api/matches/player={player_id}/?season={season_id}

### Example request:

```
const get_players = async() =>{
const response = await fetch('https://football-players-stats-api.herokuapp.com/api/players/1',{
headers:{
 Authorization: `token ${your_token}`
 }
 })
} const data = await response.json(}
```

### Example response:
```
{
  "id":1,
  "name":"Lionel Messi",
  "age":"34",
  "date_of_birth":"1987-06-24",
  "nationality":"Argentina",
  "club":"Paris St-G.",
  "height":"1.68m"
}
```
