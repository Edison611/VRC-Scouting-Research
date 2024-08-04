import json
import time
from helper import fetch_data, append_to_json_file

# THIS IS FOR THE OVER UNDER SEASON

# Remember to Change File Paths (IMPORTANT)

# Fetch from API
def store_event_ids():
    season_id = 181  # OVER UNDER ID
    rj = fetch_data(f'https://www.robotevents.com/api/v2/seasons/{season_id}/events?per_page=250')

    events = rj['data']

    # Go through each page
    pages = rj['meta']['last_page']
    for page in range(2, pages+1):
        rj = fetch_data(f'https://www.robotevents.com/api/v2/seasons/{season_id}/events?page={page}&per_page=250')
        events = events + rj['data']

    # Get Each Events Id
    ids = set()
    for event in events:
        ids.add(event['id'])
    ids = list(ids)
    with open('event_data.json', 'w') as json_file:
        json.dump(ids, json_file, indent=4)


def format_data(data):
    formatted = []
    for i in data:
        formatted.append({"round": i["round"], "alliances": i["alliances"]})
    return formatted


def store_match_data():
    ids = json.load(open('event_data.json'))
    current_index = json.load(open('match_data.json'))
    current_index = current_index["current_index"]
    for i in range(current_index, len(ids)):
        event_id = ids[i]
        print(f"Fetching event: {event_id}")
        matches = []
        while True:
            try:
                rj = fetch_data(f'https://www.robotevents.com/api/v2/events/{event_id}')
                if not rj:
                    raise ValueError("No data found")
                if 'divisions' not in rj:
                    break

                # Adding match data for each division
                for division in rj['divisions']:
                    # fetch first page to get total num of pages required
                    match_rj = fetch_data(f"https://www.robotevents.com/api/v2/events/{event_id}/divisions/{division['id']}/matches?per_page=250")
                    if not match_rj:
                        raise ValueError("No match data found")
                    pages = match_rj['meta']['last_page']
                    matches = matches + match_rj['data']
                    for page in range(2, pages+1):
                        match_rj = fetch_data(f"https://www.robotevents.com/api/v2/events/{event_id}/divisions/{division['id']}?page={page}&per_page=250")
                        # print(match_rj)
                        if not match_rj:
                            break
                        if 'data' in match_rj:
                            matches = matches + match_rj['data']
                break
            except ValueError as e:
                print(f"Error: {e}. Waiting for 5 minutes before retrying...")
                time.sleep(300)  # Wait for 300 seconds (5 minutes)

        # Format Data so that we only keep useful info
        matches = format_data(matches)
        append_to_json_file("match_data.json", matches)
        print(f"Number of Events Completed: {i}")


# store_event_ids()
# store_match_data()
data = json.load(open('match_data.json'))
print(len(data['matches']))
