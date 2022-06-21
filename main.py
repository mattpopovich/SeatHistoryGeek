

""" 
Date: June 20, 2022
Author: Matt Popovich
About: TODO
TODO: Everything 
""" 

import urllib # Website connections
import configparser
import json
import requests

config = configparser.ConfigParser()
config_filename = "config.cfg"
config.read(config_filename)

print(f"config client id: {config['DEFAULT']['Client_ID']}")

client_id = config['DEFAULT']['Client_ID']
secret = config['DEFAULT']['Secret']


query = 'https://api.seatgeek.com/2/events?performers.slug=colorado-avalanche' + '&client_id=' + client_id + '&client_secret=' + secret

print(query)

# import requests
# r = requests.get('https://github.com/timeline.json')
# r.json()

# extracting data
req = urllib.request.Request(query, headers = {'User-Agent':'Mozilla/5.0'})
json_data = json.load(urllib.request.urlopen(req))

print(json.dumps(json_data, indent=4))

