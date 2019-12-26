import requests
import config

headers = {'X-Auth-Token': config.football_api_token}
# https://www.football-data.org/documentation/quickstart
# mt_key = 0   # match_day key
football_key = {'status': 0, 'key': ''}
football_dict = {0: ['Serie A', 'Italy'],
                 1: ['Primera Division', 'Spain'],
                 2: ['Eredivisie', 'Netherlands'],
                 3: ['FIFA World Cup', 'World'],
                 4: ['Ligue 1', 'France'],
                 5: ['Bundesliga', 'Germany'],
                 6: ['Primeira Liga', 'Portugal'],
                 7: ['Premier League', 'England'],
                 8: ['European Championship', 'Europe'],
                 9: ['UEFA Champions League', 'Europe'],
                 10: ['Championship', 'England']
                 }
competition_ids = ['Série A', 'Primera Division', 'Eredivisie',
                   'Primera Division', 'Ligue 1', 'Bundesliga',
                   'Primeira Liga', 'Premier League']

# THIS CODE MATCHES THE FOOTBALL_DICT KEYS
league_code = {0: 'SA',
               1: 'PD',
               2: 'DED',
               3: 'WC',
               4: 'FL1',
               5: 'BL1',
               6: 'PPL',
               7: 'PL',
               8: 'CL',
               9: 'EL',
               10: 'ELC'
               }


def which_league(_key):
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
    football_key['status'] = 1
    football_key['key'] = _key
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
        _id = football_dict[msg][0]
    except KeyError:
        return "invalid key\n" + which_league(football_key['key'])

    req = requests.get("https://api.football-data.org/v2/matches", headers=headers)
    data = req.json()
    scores = ''

    for i in data['matches']:
        if i['competition']['name'] == _id:
            team1 = i['homeTeam']['name']
            team2 = i['awayTeam']['name']
            s_team1 = i['score']['fullTime']['homeTeam']
            s_team2 = i['score']['fullTime']['awayTeam']
            result = f"{team1} {s_team1} vs {s_team2} {team2}\n"
            scores += result
    if scores != '':
        football_key['status'] = 0
        football_key['key'] = ''
        # mt_key = 0
        return scores
    else:
        # mt_key = 0
        football_key['status'] = 0
        football_key['key'] = ''
        return f"There is no games today for {_id}"


def match_base(_league_code, match_day):
    req = requests.get(f"https://api.football-data.org/v2/competitions/{_league_code}/matches?matchday={match_day}",
                       headers=headers)
    data = req.json()

    return data


def match_schedules(msg):
    global football_key
    global match_id

    code = league_code[msg]
    try:
        data = match_base(code, match_id)
        scores = f'{data["competition"]["name"]} Match Schedules for Game {match_id}:\n'

        for i in data['matches']:
            if i['status'] == 'FINISHED':
                team1 = i['homeTeam']['name']
                team2 = i['awayTeam']['name']
                s_team1 = i['score']['fullTime']['homeTeam']
                s_team2 = i['score']['fullTime']['awayTeam']
                result = f"{team1} {s_team1} vs {s_team2} {team2}\n"
                scores += result
            else:
                team1 = i['homeTeam']['name']
                team2 = i['awayTeam']['name']
                result = f"{team1} vs {team2}\n"
                scores += result
        football_key['status'] = 0
        football_key['key'] = ''
        match_id = ''
        return scores
    except Exception as e:
        football_key['status'] = 0
        football_key['key'] = ''
        match_id = ''
        return e


# primeier league start
def league_start(msg):
    global football_key

    code = league_code[msg]
    data = match_base(code, 1)

    football_key['status'] = 0
    football_key['key'] = ''
    return data['matches'][0]['season']['startDate']


def season_status(msg):  # 'key_code = ss_key'
    global football_key

    try:
        code = league_code[msg]
        data = match_base(code, 1)

        football_key['status'] = 0
        football_key['key'] = ''

        league_name = data['competition']['name']
        start = data['matches'][0]['season']['startDate']
        end = data['matches'][0]['season']['endDate']
        cmd = data['matches'][0]['season']['currentMatchday']
        reply = f"{league_name} Season Status: \nSeason started on {start} and will end on {end}.\n" \
                f"The current match day is {cmd}"

        return reply

    except Exception as e:
        return e


# print(match_today_(7))
# print(match_schedules_pl(11))
function_call = {'mt_key': match_today_, 'ms_key': match_schedules, 'ls_key': league_start, 'ss_key': season_status}
match_id = ''


def football_switch(msg):
    try:
        code = int(msg)
    except ValueError:
        return "invalid key\n" + which_league(football_key['key'])
    fc = football_key['key']
    return function_call[fc](code)


def football(message):
    global match_id
    if message == 'football match today':
        return which_league('mt_key')
    elif message == 'football league start':
        return which_league('ls_key')
    elif message == 'football league status':
        return which_league('ss_key')
    elif message[:28] == 'football match schedules for':
        match_id = message.split()[-1]
        return which_league('ms_key')

# football match today
# football league start
# football league status
# football match schedules for match 11
# print(season_status(7))