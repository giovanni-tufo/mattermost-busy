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


def set_status(current_icon, current_status, custom_status_text):
    client = mattermostdriver.Driver({
        'url': os.getenv('MATTERMOST_URL'),
        'token': os.getenv('MATTERMOST_TOKEN'),
        'port': int(os.getenv('MATTERMOST_PORT'))
    })
    client.login()
    options = client.users.get_user(user_id='me')
    options['props']['customStatus'] = "{\"emoji\":\"" + current_icon + "\",\"text\":\"" + custom_status_text + "\"}"

    client.users.update_user(user_id='me', options=options)

    user_status_options = {
        "user_id": options['id'],
        "status": current_status
    }

    client.status.update_user_status(user_id='me', options=user_status_options)


now = datetime.now()
today = now.strftime("%d/%m")
weekday = int(now.strftime("%w"))
current_hour = int(now.strftime("%H"))
current_minute = int(now.strftime("%M"))
customStatusText = today + ' meetings (▓ busy): '
ceil = str(math.floor(current_minute / 15) * 15)
currentIcon = os.getenv('MATTERMOST_FREE_EMOJI', 'house_with_garden')
if weekday == 5:
    currentIcon = os.getenv('MATTERMOST_FRIDAY_EMOJI', 'parrot')
currentStatus = 'online'
with open(join(dirname(__file__), 'meetings.json')) as json_file:
    data = json.load(json_file)
    if 'AWAY' in data:
        currentIcon = os.getenv('MATTERMOST_AWAY_EMOJI', 'beach_umbrella')
        currentStatus = 'offline'
        customStatusText = 'On holiday, I will return on ' + data['AWAY']
        set_status(currentIcon, currentStatus, customStatusText)
        exit()
    if str(current_hour) not in data:
        currentStatus = 'offline'
        currentIcon = os.getenv('MATTERMOST_OFF_EMOJI', 'sleeping')
        customStatusText = 'See you at 9'
        if current_hour > int(os.getenv('MATTERMOST_END_HOUR', '18')) and weekday != 5:
            customStatusText = 'See you tomorrow at 9'
        elif weekday == 5:
            customStatusText = 'See you on Monday at 9'
        set_status(currentIcon, currentStatus, customStatusText)
        exit()
    if data[str(current_hour)][str(ceil)] == 'BUSY':
        currentIcon = os.getenv('MATTERMOST_BUSY_EMOJI', 'calendar')
        currentStatus = 'dnd'
    if data[str(current_hour)][str(ceil)] == 'MEAL':
        currentIcon = os.getenv('MATTERMOST_MEAL_EMOJI', 'pizza')
        currentStatus = 'away'
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

customStatusText += os.getenv('MATTERMOST_END_HOUR', '18')
set_status(currentIcon, currentStatus, customStatusText)