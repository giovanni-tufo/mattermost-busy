# coding=UTF-8
import math
import os
from datetime import datetime
from os.path import join, dirname
import json
import mattermostdriver
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

now = datetime.now()
today = now.strftime("%d/%m")
weekday = int(now.strftime("%w"))
current_hour = int(now.strftime("%H"))
current_minute = int(now.strftime("%M"))
customStatusText = today + ' meetings (▓ busy): '
ceil = str(math.floor(current_minute/15) * 15)
currentIcon = os.getenv('MATTERMOST_FREE_EMOJI')
if weekday == 5:
    currentIcon = os.getenv('MATTERMOST_FRIDAY_EMOJI')
currentStatus = 'online'
with open(join(dirname(__file__), 'meetings.json')) as json_file:
    data = json.load(json_file)
    if data[str(current_hour)][str(ceil)] == 'BUSY':
        currentIcon = os.getenv('MATTERMOST_BUSY_EMOJI')
        currentStatus = 'dnd'
    for hour in data:
        customStatusText += hour
        for minute in data[hour]:
            status = data[hour][minute]
            if int(hour) < current_hour or (int(hour) == current_hour and current_minute > int(minute) != int(ceil)):
                customStatusText += '▒'
                continue
            if int(hour) == current_hour and int(minute) == int(ceil) and currentStatus != 'online':
                customStatusText += '▓'
                continue
            if status == 'FREE':
                customStatusText += '░'
            else:
                customStatusText += '▓'

customStatusText += os.getenv('MATTERMOST_END_HOUR')
client = mattermostdriver.Driver({
    'url': os.getenv('MATTERMOST_URL'),
    'token': os.getenv('MATTERMOST_TOKEN'),
    'port': int(os.getenv('MATTERMOST_PORT'))
})

client.login()

options = client.users.get_user(user_id='me')

options['props']['customStatus'] = "{\"emoji\":\"" + currentIcon + "\",\"text\":\"" + customStatusText + "\"}"

props = client.users.update_user(user_id='me', options=options)

userStatusOptions = {
    "user_id": options['id'],
    "status": currentStatus
}

user_status = client.status.update_user_status(user_id='me', options=userStatusOptions)

print(customStatusText)