import requests
import json

# THIS IS FOR THE OVER UNDER SEASON

# Remember to Change File Paths (IMPORTANT)

# Dump all data into a json file
# ---------------------------------
season_id = 181 # OVER UNDER ID
url = 'https://vrc-data-analysis.com/v1/historical_allteams/' + str(season_id)
r = requests.get(url, headers={})
rj = r.json()

formatted = {}
for team in rj:
    formatted[team['team_number']] = team
with open('team_data.json', 'w') as json_file:
    json.dump(formatted, json_file, indent=4)
