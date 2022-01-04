const icon = document.querySelector('.toggle')
const menu = document.querySelector(".navegation")
icon.addEventListener("click",function(){
    menu.classList.toggle('view')
})




var div = document.querySelector('.data')

const token = "b6f28d7fc1c6d63567a7181a12c6aa8dae59598";

const get_players = async() =>{
const response = await fetch('https://football-players-stats-api.herokuapp.com/api/matches/player=1/?season=18',{
    headers: {
        Authorization: `token ${token}`
    }
})
const data = await response.json()  

var list = data
var list = list.slice(-5)
    for (var i in list){          
        var item = 
        `
        <tr>                     
        <td>${list[i].date}</td>
        <td>${list[i].competition}</td>
        <td>${list[i].home_team}</td>
        <td>${list[i].result}</td>
        <td>${list[i].away_team}</td>
        <td>${list[i].goals}</td>
        </tr>          
        `
        div.innerHTML += item
    }
}
get_players()
