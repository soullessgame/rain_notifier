import requests
import pandas as pd
import yaml

def read_yaml(yaml_path):
    with open(yaml_path, 'r',encoding='utf-8') as f:
        yaml_content = yaml.safe_load(f)
    return yaml_content

config_path = "configs/config.yml"
configs = read_yaml(config_path)


#get data from API
API_KEY = configs["API_KEY"]
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