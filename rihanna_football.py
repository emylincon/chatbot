import requests
import config

headers = {'X-Auth-Token': config.football_api_token}
# https://www.football-data.org/documentation/quickstart
football_key = 0
football_dict = {0:['Serie A', 'Italy'],
                 1:['Primera Division', 'Spain'],
                 2:['Eredivisie', 'Netherlands'],
                 3:['FIFA World Cup', 'World'],
                 4:['Ligue 1', 'France'],
                 5:['Bundesliga', 'Germany'],
                 6:['Primeira Liga', 'Portugal'],
                 7:['Premier League', 'England'],
                 8:['European Championship', 'Europe'],
                 9:['UEFA Champions League', 'Europe'],
                 10:['Championship', 'England']
                 }
competition_ids = ['Série A', 'Primera Division', 'Eredivisie',
                       'Primera Division', 'Ligue 1', 'Bundesliga',
                       'Primeira Liga', 'Premier League']


def which_league():
    global football_key
    reply = "<table>\
              <tr>\
                <th>Key</th>\
                <th>League</th>\
                <th>Place</th>\
              </tr>\
            "
    for i in football_dict:
        reply += f"<tr>\
                    <td>{i}</td>\
                    <td>{football_dict[i][0]}</td>\
                    <td>{football_dict[i][1]}</td>\
                  </tr>"
    reply += "</table>~<br> Please Enter a Key"
    '''
    reply = '~| Key     \t | League \t | Place   \t |'
    s = len(str(reply))
    reply+='\n'
    for i in range(s):
        reply += '-'

    for i in football_dict:
        reply+=f'\n| {i}     \t | {football_dict[i][0]} \t | {football_dict[i][1]}   \t |'
    '''
    football_key = 1
    return reply



def match_today():
    # Premier League Matches Only
    req = requests.get("https://api.football-data.org/v2/matches", headers=headers)
    data = req.json()
    scores = ''
    for i in data['matches']:

        if i['competition']['name'] == 'Premier League':
            team1 = i['homeTeam']['name']
            team2 = i['awayTeam']['name']
            s_team1 = i['score']['fullTime']['homeTeam']
            s_team2 = i['score']['fullTime']['awayTeam']
            result = f"{team1} {s_team1} - {s_team2} {team2}\n"
            scores += result

    return scores


def match_today_(msg):
    global football_key

    try:
        msg = int(msg)
        _id = football_dict[msg][0]
    except KeyError:
        return "invalid key\n" + which_league()

    req = requests.get("https://api.football-data.org/v2/matches", headers=headers)
    data = req.json()
    scores = ''

    for i in data['matches']:
        if i['competition']['name'] == _id:
            team1 = i['homeTeam']['name']
            team2 = i['awayTeam']['name']
            s_team1 = i['score']['fullTime']['homeTeam']
            s_team2 = i['score']['fullTime']['awayTeam']
            result = f"{team1} {s_team1} <-> {s_team2} {team2}\n"
            scores += result
    if scores != '':
        football_key = 0
        return scores
    else:
        football_key = 0
        return f"There is no games today for {_id}"

#print(match_today_(7))
