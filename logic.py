import json
import csv
from datetime import datetime

# CHANGE ME IF YOU WANT TO CHANGE JSON PATH
json_file_path = 'new.json'

# Sort function
def custom_sort_key(event_result):
    set_info = event_result['eventResponseData']['sets'][0]  
    encounter_info = set_info['encounters'][0] 

    return (
        event_result.get('eventId', 'N/A'),
        event_result.get('eventResultType', 'N/A'),
        encounter_info.get('type', 'N/A'),
        encounter_info.get('enemyHp', 'N/A'),
        encounter_info['battleContributions'][0].get('damageDealt', 'N/A'),
        encounter_info['battleContributions'][0].get('damageType', 'N/A'),
        encounter_info['battleContributions'][0].get('completedOn', 'N/A')
    )

# Open JSON file and load it to data
with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

# Extract the list under 'eventResults' key
event_results = data.get('eventResults', [])

# Sort the data based on the custom key
sorted_data = sorted(event_results, key=custom_sort_key)

# Print the sorted data
for event_result in sorted_data:
    event_id = event_result.get('eventId', 'N/A')
    event_result_type = event_result.get('eventResultType', 'N/A')

    set_info = event_result.get('eventResponseData', {}).get('sets', [])[0]
    encounter_info = set_info.get('encounters', [])[0]

    encounter_type = encounter_info.get('type', 'N/A')
    enemy_hp = encounter_info.get('enemyHp', 'N/A')

    damage_dealt = encounter_info['battleContributions'][0].get('damageDealt', 'N/A')
    damage_type = encounter_info['battleContributions'][0].get('damageType', 'N/A')
    completed_on = encounter_info['battleContributions'][0].get('completedOn', 'N/A')

    print(
        f"Event ID: {event_id}, "
        f"Event Result Type: {event_result_type}, "
        f"Encounter Type: {encounter_type}, "
        f"Enemy HP: {enemy_hp}, "
        f"Damage Dealt: {damage_dealt}, "
        f"Damage Type: {damage_type}, "
        f"Completed On: {completed_on}"
    )

current_datetime = datetime.now().strftime('%Y%m%d%H%M%S')
csv_file_path = f'output_{current_datetime}.csv'

with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header row
    csv_writer.writerow(['Event ID', 'Event Result Type', 'Encounter Type', 'Crystal Type', 'Enemy HP', 'User ID', 'Damage Dealt', 'Damage Type', 'Completed On'])

    # Write data rows
    for event_result in sorted_data:
        event_id = event_result.get('eventId', 'N/A')
        event_result_type = event_result.get('eventResultType', 'N/A')

        set_info = event_result.get('eventResponseData', {}).get('sets', [])[0]
        
        for encounter_info in set_info['encounters']:
            encounter_type = encounter_info.get('type', 'N/A')
            enemy_hp = encounter_info.get('enemyHp', 'N/A')
            encounter_id = encounter_info.get('encounterId', 'N/A')

            # Loop through each user's contribution
            for contribution in encounter_info['battleContributions']:
                user_id = contribution.get('userId', 'N/A')
                damage_dealt = contribution.get('damageDealt', 'N/A')
                damage_type = contribution.get('damageType', 'N/A')
                completed_on = contribution.get('completedOn', 'N/A')

                csv_writer.writerow([event_id, event_result_type, encounter_type, encounter_id, enemy_hp, user_id, damage_dealt, damage_type, completed_on])

print(f'CSV file saved at: {csv_file_path}')
