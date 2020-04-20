#! python3

import webbrowser as web
import requests
import json
from datetime import date
from datetime import datetime



youtube_api_key = 'YOUR_API_KEY'
my_channel = 'YOUR_CHANNEL_ID'




channels_ids = []
active_channels_ids = []

# Obtener las ids de los canales que estoy suscrito y meterlos en channels_ids
def get_subs_channels():
    get_subscription = f'https://www.googleapis.com/youtube/v3/subscriptions?part=snippet&channelId={ my_channel }&maxResults=10&key={ youtube_api_key }'
    response_sub = requests.get(get_subscription)
    json_sub = response_sub.json()
    num_subscriptions = json_sub['pageInfo']['totalResults']
    range_subscriptions = range(0, num_subscriptions)
    def range_subs():
        for sub in range_subscriptions:
            get_ids = json_sub['items'][sub]['snippet']['resourceId']['channelId']
            channels_ids.append(get_ids)
    range_subs()
    
get_subs_channels()


# Obtener las ids de los canales que han subido video después de x tiempo 

def get_subs_activities():
    with open('data.json') as file: # Abriendo el archivo data.json y tomando la fecha actual
        data = json.load(file)
        for i in channels_ids:
            get_activity = f'https://www.googleapis.com/youtube/v3/activities?part=snippet&channelId={ channels_ids[i] }&publishedAfter={ data["lastDate"][0]["lastLocalDate"] }&key={ youtube_api_key }'
            response_act = requests.get(get_activity)
            json_act = response_act.json()
            num_act = json_act['pageInfo']['totalResults']
            range_act = range(0, num_act)
            def take_ids():
                for act in range_act:
                    channel_active_id = json_act['items'][act]['snippet']['channelId'] 
                    active_channels_ids.append(channel_active_id)
            take_ids()
get_subs_activities()

def get_local_date():
    today = date.today()
    now = datetime.now()
    por = '%3A'
    data = {}
    data['lastDate'] = []
    data['lastDate'].append({
        'lastLocalDate': f'{today}T{now.hour}{por}{now.minute}{por}{now.second}.000Z'
    })
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=3)    
get_local_date()
 



def launch_browser():
    if len(active_channels_ids) != 0:
        for channel in active_channels_ids:
            url = f'https://www.youtube.com/channel/{ active_channels_ids[channel] }'
            web.open(url, new=1, autoraise=True)
    else:
        exit()
        
launch_browser()
    



        
    
