# -----------------------------------------------------------------------------
# Name:        retrieveSkillsData
# Purpose:     Retrieves the skills' data for all teams in a tournament
#
# Author:      Yash Kothari
# Created:     2023
# Updated:     2023
# -----------------------------------------------------------------------------

import requests
import json

# season_id = 173 #spin up
season_id = 181  # over under

# To get event id: use this link https://www.robotevents.com/api/v2/teams/140100/events?season%5B%5D=181
# which gets all events capybaras will be in, then for the desired event, set event_id to the event's id
# event_id = 51483  # speedway event_id
event_id = 51923 # berkeley event_id
team_id = 140100  # 2055A team id
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiMjE5MmEyY2U3NjhlZWViNTRlMTQ1NTMzNGUwZDZhZDdjM2IyMjVkZDllZDRlNGQxYjFmYzIxNzU2ZTJhY2Q5ZjdhODllOTlkNzA3OGMyYTciLCJpYXQiOjE2NzI3NTg0ODguNjgzMDE3LCJuYmYiOjE2NzI3NTg0ODguNjgzMDIwMSwiZXhwIjoyNjE5NTI5Njg4LjY3NzI3MDksInN1YiI6IjExMDgzMiIsInNjb3BlcyI6W119.UPXqld7tHv6sRyUufI6VWQR09NbGa65gjf-Epsjwdd0HCqhlOUB8SRCONBUYkqsO8FuH4MgsLq0m4g5QTlwfNMqq3aRfpTBePJI4eawBTOQY7u5fk7hgWDcPXHng08IVeCFyopJl6Zy4MVTVslVqiZmgc43Vz9A9mwTtGSRhmZD_AqOmN2tYbP8y63pfjEpJ2X-gqo0416cRj95FeNLUMDSUZBpQHRWoXfrQAUxaj6qfxKar0eLDTWjAGkpMkKa28HWTYmkbajgSKPh23ubtRWWq_z152Oum5zQcdPzPZZrkrCvH9h2o0pCt3sr3zrEVMNeN96bf-e9oD1b-CY6Tk7PCTCdecxJe5DcFVLOdCqOpIjdtVbzNWHKtltDI5ttqHGGl03RdGrdNKbKveT5xAC2TDnakJiNIwANbtPq7Wj3V-doLTAJP2w8U97dQM_G7CrBBdgMlXkUwdq1gEqQr0bCrD3z9CBwg3S2RmQjBIpS7EkrnlU_wBPzYk0RAlaT_UXgqDUiy47fax7asy8LIgiy5odXxA0xXgw34BOBp1GGk5FREnaJ61Gl_R6W99RFcR1b_uxAMscl5hgdGYG63nv7vfAcMuOxotHvd-Fc-ram3n3jBawgiecOxaJyhE2asQtm-wOKynTi5-vniX_54GtIF49OhpGT9ZeefLEudeRo'
headers = {'Accept': 'application/json', "Authorization": "Bearer " + token}
url = 'https://www.robotevents.com/api/v2/events/' + str(event_id) + '/teams?&per_page=1000'
r = requests.get(url, headers=headers)
print(r.content)
rj = r.json()
teams = (rj['data'])
for team in teams:
    # print(team)
    team_id = team['id']

    url = 'https://www.robotevents.com/api/v2/teams/' + str(team_id) + '/skills?season%5B%5D=' + str(season_id)
    r = requests.get(url, headers=headers)
    rj = r.json()
    skills = rj['data']
    bestProg = 0
    bestDriv = 0
    for skill in skills:
        if skill['type'] == 'driver':
            if skill['score'] > bestDriv: bestDriv = skill['score']
        else:
            if skill['score'] > bestProg: bestProg = skill['score']

    print(team['number'], bestDriv, bestProg, bestDriv + bestProg, team['grade'])

# this code will paste the data into the terminal
# copy and paste into google sheets, add headings like in last year's sheets
# go to Data->Split text to columns
# go to Data->Sort sheet, and sort by the total skills column
