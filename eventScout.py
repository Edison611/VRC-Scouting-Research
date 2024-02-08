# -----------------------------------------------------------------------------
# Name:        eventScout
# Purpose:     To scout for alliance and opposing teams when match schedules are released
#
# Author:      Edison Ying
# Created:     23-Dec-2023
# Updated:     24-Jan-2024
# -----------------------------------------------------------------------------
import requests
import json
import pandas as pd

# Data as of Jan 24th

file = 'canadianOpenData.xlsx'
df = pd.read_excel(f'./eventData/{file}')

event_id = 51493  # Canadian Open
# eventSKU = input("Enter Event SKU: ")
# with open('./name-id/eventSKU-id.json', 'r') as f:
#     event_ids = json.load(f)
# event_id = event_ids[eventSKU]

# team_id = 140100  # 2055A
# team_id = 154288  # 2055X
teamNumber = input("Enter Team Number: ")
with open('./name-id/teamName-id.json', 'r') as f:
    team_ids = json.load(f)
team_id = team_ids[teamNumber]

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiMjE5MmEyY2U3NjhlZWViNTRlMTQ1NTMzNGUwZDZhZDdjM2IyMjVkZDllZDRlNGQxYjFmYzIxNzU2ZTJhY2Q5ZjdhODllOTlkNzA3OGMyYTciLCJpYXQiOjE2NzI3NTg0ODguNjgzMDE3LCJuYmYiOjE2NzI3NTg0ODguNjgzMDIwMSwiZXhwIjoyNjE5NTI5Njg4LjY3NzI3MDksInN1YiI6IjExMDgzMiIsInNjb3BlcyI6W119.UPXqld7tHv6sRyUufI6VWQR09NbGa65gjf-Epsjwdd0HCqhlOUB8SRCONBUYkqsO8FuH4MgsLq0m4g5QTlwfNMqq3aRfpTBePJI4eawBTOQY7u5fk7hgWDcPXHng08IVeCFyopJl6Zy4MVTVslVqiZmgc43Vz9A9mwTtGSRhmZD_AqOmN2tYbP8y63pfjEpJ2X-gqo0416cRj95FeNLUMDSUZBpQHRWoXfrQAUxaj6qfxKar0eLDTWjAGkpMkKa28HWTYmkbajgSKPh23ubtRWWq_z152Oum5zQcdPzPZZrkrCvH9h2o0pCt3sr3zrEVMNeN96bf-e9oD1b-CY6Tk7PCTCdecxJe5DcFVLOdCqOpIjdtVbzNWHKtltDI5ttqHGGl03RdGrdNKbKveT5xAC2TDnakJiNIwANbtPq7Wj3V-doLTAJP2w8U97dQM_G7CrBBdgMlXkUwdq1gEqQr0bCrD3z9CBwg3S2RmQjBIpS7EkrnlU_wBPzYk0RAlaT_UXgqDUiy47fax7asy8LIgiy5odXxA0xXgw34BOBp1GGk5FREnaJ61Gl_R6W99RFcR1b_uxAMscl5hgdGYG63nv7vfAcMuOxotHvd-Fc-ram3n3jBawgiecOxaJyhE2asQtm-wOKynTi5-vniX_54GtIF49OhpGT9ZeefLEudeRo'
headers = {'Accept': 'application/json', "Authorization": "Bearer " + token}
url = f'https://www.robotevents.com/api/v2/events/{event_id}/divisions/1/matches?team%5B%5D={team_id}'
r = requests.get(url, headers=headers)
rj = r.json()
matches = (rj['data'])

i = 1
desiredInfo = ['teamNumber', 'tsRanking', 'awpPerMatch', 'scoreAutoMax', 'scoreTotalMax']

for match in matches:
    print('-----------------------------------------------------------------------------------------------------------')
    print(str(match["name"]) + " | " + "Match " + str(i))
    print('-----------------------------------------------------------------------------------------------------------')

    alliance = []
    opponents = []
    if match["alliances"][0]["teams"][0]["team"]["id"] == team_id:
        alliance.append(match["alliances"][0]["teams"][1]["team"]["name"])

        opponents.append(match["alliances"][1]["teams"][0]["team"]["name"])
        opponents.append(match["alliances"][1]["teams"][1]["team"]["name"])

    elif match["alliances"][0]["teams"][1]["team"]["id"] == team_id:
        alliance.append(match["alliances"][0]["teams"][0]["team"]["name"])

        opponents.append(match["alliances"][1]["teams"][0]["team"]["name"])
        opponents.append(match["alliances"][1]["teams"][1]["team"]["name"])

    elif match["alliances"][1]["teams"][0]["team"]["id"] == team_id:
        alliance.append(match["alliances"][1]["teams"][1]["team"]["name"])

        opponents.append(match["alliances"][0]["teams"][0]["team"]["name"])
        opponents.append(match["alliances"][0]["teams"][1]["team"]["name"])
    else:
        alliance.append(match["alliances"][1]["teams"][0]["team"]["name"])

        opponents.append(match["alliances"][0]["teams"][0]["team"]["name"])
        opponents.append(match["alliances"][0]["teams"][1]["team"]["name"])

    a = df[(df['teamNumber'].isin([alliance[0]]))]

    blank = pd.DataFrame(df, index=["/"])
    blank = blank.fillna("/")

    o = df[(df['teamNumber'].isin([opponents[0], opponents[1]]))]

    frames = [a, blank, o]

    result = pd.concat(frames, ignore_index=True)
    result = result.get(desiredInfo)
    result.rename(index={0: "alliance1", 1: "/", 2: "opponent1", 3: "opponent2"}, inplace=True)
    print(result.to_string())

    i += 1