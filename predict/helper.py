import requests
import json


def fetch_data(url):
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzIiwianRpIjoiMjE5MmEyY2U3NjhlZWViNTRlMTQ1NTMzNGUwZDZhZDdjM2IyMjVkZDllZDRlNGQxYjFmYzIxNzU2ZTJhY2Q5ZjdhODllOTlkNzA3OGMyYTciLCJpYXQiOjE2NzI3NTg0ODguNjgzMDE3LCJuYmYiOjE2NzI3NTg0ODguNjgzMDIwMSwiZXhwIjoyNjE5NTI5Njg4LjY3NzI3MDksInN1YiI6IjExMDgzMiIsInNjb3BlcyI6W119.UPXqld7tHv6sRyUufI6VWQR09NbGa65gjf-Epsjwdd0HCqhlOUB8SRCONBUYkqsO8FuH4MgsLq0m4g5QTlwfNMqq3aRfpTBePJI4eawBTOQY7u5fk7hgWDcPXHng08IVeCFyopJl6Zy4MVTVslVqiZmgc43Vz9A9mwTtGSRhmZD_AqOmN2tYbP8y63pfjEpJ2X-gqo0416cRj95FeNLUMDSUZBpQHRWoXfrQAUxaj6qfxKar0eLDTWjAGkpMkKa28HWTYmkbajgSKPh23ubtRWWq_z152Oum5zQcdPzPZZrkrCvH9h2o0pCt3sr3zrEVMNeN96bf-e9oD1b-CY6Tk7PCTCdecxJe5DcFVLOdCqOpIjdtVbzNWHKtltDI5ttqHGGl03RdGrdNKbKveT5xAC2TDnakJiNIwANbtPq7Wj3V-doLTAJP2w8U97dQM_G7CrBBdgMlXkUwdq1gEqQr0bCrD3z9CBwg3S2RmQjBIpS7EkrnlU_wBPzYk0RAlaT_UXgqDUiy47fax7asy8LIgiy5odXxA0xXgw34BOBp1GGk5FREnaJ61Gl_R6W99RFcR1b_uxAMscl5hgdGYG63nv7vfAcMuOxotHvd-Fc-ram3n3jBawgiecOxaJyhE2asQtm-wOKynTi5-vniX_54GtIF49OhpGT9ZeefLEudeRo'
    headers = {'Accept': 'application/json', "Authorization": "Bearer " + token}
    r = requests.get(url, headers=headers)
    if not r:
        return None
    rj = r.json()
    return rj


def append_to_json_file(file_path, new_data):
    try:
        # Read existing data from the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Ensure 'games' is a list
        if "matches" in data and isinstance(data["matches"], list):
            # Append the new game data to the 'games' list
            data["matches"] = data["matches"] + new_data
        else:
            # Initialize 'games' as a list if not present
            data["matches"] = [new_data]

        # Update metadata (e.g., increment the total_games count)
        if "current_index" in data:
            data["current_index"] += 1
        else:
            data["current_index"] = 1

    except FileNotFoundError:
        # Initialize the structure if the file does not exist
        data = {
            "current_index": 1,
            "matches": [new_data],
        }
    except json.JSONDecodeError:
        # Handle case where JSON is empty or invalid
        data = {
            "current_index": 1,
            "matches": [new_data],
        }

    # Write updated data back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

