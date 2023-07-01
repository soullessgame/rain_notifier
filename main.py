import requests
import pandas as pd
import yaml


def read_yaml(yaml_path):
    """
    Read and return Yaml file content
    """
    with open(yaml_path, 'r',encoding='utf-8') as f:
        yaml_content = yaml.safe_load(f)
    return yaml_content

def check_rain(df):
  """Check if the dataframe contains rain records"""
  for index, row in df.head(4).iterrows():
    if int(row['id'])<700:
        return True
  return False  

#TODO Send email to user
def send_rain_message(email):
   #code
   return
 

def main():
  """
  Main function
  """
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

  api_url= "https://api.openweathermap.org/data/2.5/forecast"
  response = requests.get(url=api_url, params=parameters)
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
  if check_rain(df):
    print('it will rain')
  else:
    print('it will not rain')

  return

if __name__ == "__main__":
    main()
