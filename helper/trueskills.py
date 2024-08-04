import requests
import json

# Dump all data into a json file
# ---------------------------------
# url = 'https://vrc-data-analysis.com/v1/historical_allteams/181'
# r = requests.get(url, headers={})
# rj = r.json()
# with open('data.json', 'w') as json_file:
#     json.dump(rj, json_file, indent=4)

f = open('../predict/data.json')
data = json.load(f)
print(data[0])