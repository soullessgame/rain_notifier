import requests
import pandas as pd
import yaml
import os
from twilio.rest import Client
from datetime import datetime

time_now = datetime.now().hour

def read_yaml(yaml_path):
    print(os.path.exists(yaml_path))
    with open(yaml_path, 'r',encoding='utf-8') as f:
        yaml_content = yaml.safe_load(f)
    return yaml_content

config_path = "configs/config.yaml"
configs = read_yaml(config_path)

#API inputs for weather and sms
API_KEY = configs["API_KEY"]
LAT = 51.866402
LONG = 4.661810
account_sid = 'AC1854b6578feac5255e9b9f845f4be119'
auth_token = configs["SMS_TOKEN"]
phone_number = configs["PHONE_NUMBER"]
sending_number = configs["SENDING_NUMBER"]

#access weather api and get rain data
parameters = {
    "lat": LAT,
    "lon": LONG,
    "appid": API_KEY
}

response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=parameters)
response.raise_for_status()
data = response.json()
forecast_list = data['list']

#change to pandas dateframe
df = pd.DataFrame.from_dict(forecast_list)
df['dt'] = pd.to_datetime(df['dt'], unit='s')
#get rid of nesting
df['weather'] = df['weather'].apply(lambda x: x[0])
df_normalized = pd.json_normalize(df['weather'])
df = pd.concat([df.drop('weather', axis=1), df_normalized], axis=1)
# print(df.head(4))
# print(list(df.columns))
# print(df['id'])

#notify me if it rains
raining = False
rain_message = ''
for index, row in df.head(4).iterrows():
    if int(row['id'])<700:
        raining = True

if raining:
    rain_message='it will rain ☂'
else:
    rain_message ='it will not rain ☀'

#set up sms-service - if it is 7 o clock, send message - Using pythonanywhere

client = Client(account_sid, auth_token)

message = client.messages.create(
    body=rain_message,
    from_= sending_number,
    to=phone_number
)

print(message.sid)