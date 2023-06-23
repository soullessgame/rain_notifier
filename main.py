import requests
import pandas as pd

#get data from API
API_KEY = "35ea3d6a2e252ceb467477df19ce297c"
LAT = 51.866402
LONG = 4.661810

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
print(df.head(4))
print(list(df.columns))
print(df['id'])

#notify me if it rains
raining = False
for index, row in df.head(4).iterrows():
    if int(row['id'])<700:
        raining = True

if raining:
    print('it will rain')
else:
    print('it will not rain')