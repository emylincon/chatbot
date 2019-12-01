import requests
import config

headers = {'X-Auth-Token': config.football_api_token}
# https://www.football-data.org/documentation/quickstart


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


def match_today_(_id):
    competition_ids = ['Serie A', 'Primera Division', 'Eredivisie',
                       'Primera Division', 'Ligue 1', 'Bundesliga',
                       'Primeira Liga', 'Premier League']

    req = requests.get("https://api.football-data.org/v2/matches", headers=headers)
    data = req.json()
    scores = ''
    if _id in competition_ids:
        for i in data['matches']:
            if i['competition']['name'] == _id:
                team1 = i['homeTeam']['name']
                team2 = i['awayTeam']['name']
                s_team1 = i['score']['fullTime']['homeTeam']
                s_team2 = i['score']['fullTime']['awayTeam']
                result = f"{team1} {s_team1} <-> {s_team2} {team2}\n"
                scores += result
        return scores
    else:
        return f"{_id} Division is not Available"
