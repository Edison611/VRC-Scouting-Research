# -----------------------------------------------------------------------------
# Name:        OPR and DPR
# Purpose:     Calculates the OPR and DPR of all teams for a specific event
#
# Author:      Edison Ying
# Created:     26-Feb-2024
# Updated:     28-Feb-2024
# -----------------------------------------------------------------------------
import numpy as np
import requests

# Sample code for Ontario HS Division 2024

event_id = 52543

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiMjE5MmEyY2U3NjhlZWViNTRlMTQ1NTMzNGUwZDZhZDdjM2IyMjVkZDllZDRlNGQxYjFmYzIxNzU2ZTJhY2Q5ZjdhODllOTlkNzA3OGMyYTciLCJpYXQiOjE2NzI3NTg0ODguNjgzMDE3LCJuYmYiOjE2NzI3NTg0ODguNjgzMDIwMSwiZXhwIjoyNjE5NTI5Njg4LjY3NzI3MDksInN1YiI6IjExMDgzMiIsInNjb3BlcyI6W119.UPXqld7tHv6sRyUufI6VWQR09NbGa65gjf-Epsjwdd0HCqhlOUB8SRCONBUYkqsO8FuH4MgsLq0m4g5QTlwfNMqq3aRfpTBePJI4eawBTOQY7u5fk7hgWDcPXHng08IVeCFyopJl6Zy4MVTVslVqiZmgc43Vz9A9mwTtGSRhmZD_AqOmN2tYbP8y63pfjEpJ2X-gqo0416cRj95FeNLUMDSUZBpQHRWoXfrQAUxaj6qfxKar0eLDTWjAGkpMkKa28HWTYmkbajgSKPh23ubtRWWq_z152Oum5zQcdPzPZZrkrCvH9h2o0pCt3sr3zrEVMNeN96bf-e9oD1b-CY6Tk7PCTCdecxJe5DcFVLOdCqOpIjdtVbzNWHKtltDI5ttqHGGl03RdGrdNKbKveT5xAC2TDnakJiNIwANbtPq7Wj3V-doLTAJP2w8U97dQM_G7CrBBdgMlXkUwdq1gEqQr0bCrD3z9CBwg3S2RmQjBIpS7EkrnlU_wBPzYk0RAlaT_UXgqDUiy47fax7asy8LIgiy5odXxA0xXgw34BOBp1GGk5FREnaJ61Gl_R6W99RFcR1b_uxAMscl5hgdGYG63nv7vfAcMuOxotHvd-Fc-ram3n3jBawgiecOxaJyhE2asQtm-wOKynTi5-vniX_54GtIF49OhpGT9ZeefLEudeRo'
headers = {'Accept': 'application/json', "Authorization": "Bearer " + token}


def fetch(url):
    """
    Fetches data from a set RobotEventsAPI url
    :param url:
    :return:
    """
    r = requests.get(url, headers=headers)
    rj = r.json()
    return rj['data']


matchData = fetch('https://www.robotevents.com/api/v2/events/' + str(event_id) + '/divisions/1/matches?&per_page=1000&round%5B%5D=2')
teamData = fetch('https://www.robotevents.com/api/v2/events/' + str(event_id) + '/teams?&per_page=1000')

# Helper Maps Initialization
numToTeam = {}
teamToNum = {}
for i in range(len(teamData)):
    info = teamData[i]
    numToTeam[i] = info['number']
    teamToNum[info['number']] = i

oprArr = []
oprScores = []

dprArr = np.array([])
dprScores = np.array([])

for match in matchData:
    if match['round'] != 2:
        continue
    r1 = [0 for i in range(len(teamData))]
    r2 = [0 for i in range(len(teamData))]
    team1, team2 = [], []
    a1 = match['alliances'][0]
    a2 = match['alliances'][1]

    t1, t2 = match['alliances'][0]['teams'][0]['team']['name'], match['alliances'][0]['teams'][1]['team']['name']
    t3, t4 = match['alliances'][1]['teams'][0]['team']['name'], match['alliances'][1]['teams'][1]['team']['name']

    r1[teamToNum[t1]], r1[teamToNum[t2]] = 1, 1
    oprArr.append(r1)
    oprScores.append(a1['score'])

    r2[teamToNum[t3]], r2[teamToNum[t4]] = 1, 1
    oprArr.append(r2)
    oprScores.append(a2['score'])

# Convert to Numpy for more vector functions
oprArr = np.array(oprArr)
oprScores = np.array(oprScores)
# print(oprArr)

# Transpose Array
oprTranspose = np.transpose(oprArr)
LS = np.matmul(oprTranspose, oprArr)
# print(LS)

# Scores of Matches Array
RS = np.matmul(oprTranspose, oprScores)
# print(RS)

x = np.linalg.lstsq(LS, RS, rcond=None)

teamsOPR = {}
for i in range(len(x[0])):
    teamsOPR[numToTeam[i]] = round(x[0][i], 3)

print(teamsOPR)
