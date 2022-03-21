import requests
import time
import csv
import datetime
from datetime import timedelta


# Access token for site
ACCESS_TOKEN = ""

#Create todays time in unix format and create original epoch time
current_epoch_time = int(time.time())
current_epoch_time = str(current_epoch_time)
og_epoch_time='86406'
num_days = 5
view_data = []
counter = 0

# Authorization Header
headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}'
}


# Loop through responses by using created date. counter goes up to num of days entered
while True:
    counter+=1
    if counter < num_days:
        lower_timestamp = int(current_epoch_time) - int(og_epoch_time)
        data_field = f"?created[lt]={current_epoch_time}&created[gt]={lower_timestamp}"
        api_base_url = "https://api.wootric.com/v1"
        endpoint_path = f"/responses/{data_field}"
        endpoint = f"{api_base_url}{endpoint_path}"
        r = requests.get(endpoint, headers=headers)
        data = r.json()
        view_data.extend(data)
        #print(r)
        print(data)
        print(f'The response url is {endpoint}')
        print(f"Day: {counter}")
        current_epoch_time = lower_timestamp
        

    if counter > num_days: 
        break

# Initialize rows with an initial header row
rows = [('ID', 'End User ID', 'Survey ID',
        'Score', 'Text', 'Completed', 'Excluded from Calculations', 'IP Address',
        'Origin URL', 'Created At', 'Updated At','Tags', 'Notes', 'End User', 'Email')]


for survey in view_data:
    row = (
        survey['id'],
        survey['end_user_id'],
        survey['survey_id'],
        survey['score'],
        survey['text'],
        survey['completed'],
        survey['excluded_from_calculations'],
        survey['ip_address'],
        survey['origin_url'],
        survey['created_at'],
        survey['updated_at'],
        survey['tags'],
        survey['notes'],
        survey['end_user'],
        survey['end_user']['email'],
    )
    rows.append(row)


with open('wootric_nps.csv', mode='w', newline='') as csv_file:
   report_writer = csv.writer(csv_file, dialect='excel')
   for row in rows:
       report_writer.writerow(row)
