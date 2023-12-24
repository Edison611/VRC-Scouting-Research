import requests
import pandas as pd

df = pd.read_excel('./eventData/hollywoodData.xlsx')

worlds = df.query('qualifiedForWorlds == 1')
worlds = worlds.get(['teamNumber', 'tsRanking', 'scoreDriverMax', 'scoreAutoMax', 'scoreTotalMax', 'qualifiedForWorlds'])
worlds = worlds.sort_values(['scoreTotalMax'], ascending=False)

print(worlds.to_string())


# headers = {'Accept': 'application/json'}
# response = requests.get("https://vrc-data-analysis.com/event/RE-VRC-23-1524", headers=headers)
# rj = response.content
#
# print(rj)