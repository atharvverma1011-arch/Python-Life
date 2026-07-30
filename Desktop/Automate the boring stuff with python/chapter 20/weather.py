import requests
import os
from datetime import datetime

api_key = os.environ['OWM_API_KEY']
#api_key = 'b950bc743a8a7be3a9d49d33bc7e3421'
city = 'Jalandhar'
ntfy_topic = 'messages'

url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
response = requests.get(url)
data = response.json()
#print(data)

#description = data['weather'][0]['description']
#temp = data['main']['temp']
today =  datetime.now().strftime('%Y-%m-%d')
rain_times = []

#print(f'Weather in {city}: {description}, {temp}')
for entry in data['list']:
    if entry['dt_txt'].startswith(today):
        description = entry['weather'][0]['description']
        if 'rain' in description.lower():
            utc_time = datetime.strptime(entry['dt_txt'], '%Y-%m-%d %H:%M:%S')
            ist_time = utc_time + timedelta(hours=5, minutes=30)
            time_only = ist_time.strftime('%H:%M')
            rain_times.append(f'{time_only} IST ({description})')

if rain_times:
    times_str = ', '.join(rain_times)
    requests.post(f'https://ntfy.sh/{ntfy_topic}',
                  data=f'Rain expected today at:{times_str}.Bring an Umbrella!',
                  headers = {'title': 'Rain Alert', 'Tags':'umbrella,rain'})
    print(f'Rain detected at:{times_str} - notification sent!')
else:
    requests.post(f'https://ntfy.sh/{ntfy_topic}',
                  data = 'No rain detected today.',
                  headers ={'Title':'Weather update','Tags':'sunny,weather'})
    print(f'No rain detected - notification sent') 

'''if 'rain' in description.lower():
    requests.post(f'https://ntfy.sh/{ntfy_topic}',
                  data='Bring an umbrella today! Rain expected.',
                  headers={'title': 'Umbrella Reminder','Tags':'umbrella,rain'})

    print('Rain detected - notification sent!')
else:
    requests.post(f'https://ntfy.sh/{ntfy_topic}',
                      data='No rain detected',
                      headers={'title': 'Umbrella Reminder','Tags':'sunny,weather'})
    print('No rain detected - notification sent')'''
