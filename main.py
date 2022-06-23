

""" 
Date:   June 20, 2022
Author: Matt Popovich (popovich.matt@gmail.com)
About:  Will grab data of every Colorado Avalanche game from SeatGeek and log 
        ticket price information
TODO:   See the various TODO's spread throughout the code 
""" 

### Imports
import urllib
import configparser
import json
import requests
import datetime     # datetime.datetime.utcnow(): datetime.datetime
import sys          # sys.exit()


### Classes

# Records a single event's information for a certain slice/period in time
class EventSlice:

    def __init__(self, full_event: dict, time_retrieved_utc: datetime.datetime):
        self.full_event = full_event
        self.parse_event(full_event)
        self.time_retrieved_utc: datetime.datetime = time_retrieved_utc

    def parse_event(self, full_event: dict):
        self.type: str = full_event['type']                                                 # "nhl"
        self.event_id: int = full_event['id']                                               # 5653481
        self.datetime_utc: str = full_event['datetime_utc']                                 # "2022-06-21T00:00:00"
        self.listing_count: int = full_event['stats']['listing_count']                      # 15
        self.lowest_price_good_deals: int = full_event['stats']['lowest_price_good_deals']  # 116
        self.lowest_price: int = full_event['stats']['lowest_price']                        # 116
        self.highest_price: int = full_event['stats']['highest_price']                      # 1009
        self.visible_listing_count: int = full_event['stats']['visible_listing_count']      # 15
        self.median_price: int = full_event['stats']['median_price']                        # 343
        self.url: str = full_event['url']                                                   # "https://seatgeek.com/colorado-avalanche-at-tampa-bay-lightning-stanley-cup-finals-game-3-tickets/6-20-2022-tampa-florida-amalie-arena/nhl/5653481"
        self.venue_id: int = full_event['venue']['id']                                      # 182
        self.score: float = full_event['score']                                             # 0.623
        self.title: str = full_event['title']                                               # "Colorado Avalanche at Tampa Bay Lightning: Stanley Cup Finals - Game 3"
        self.performer0name: str = full_event['performers'][0]['name']                      # "Tampa Bay Lightning"
        self.performer1name: str = full_event['performers'][1]['name']                      # "Colorado Avalanche"

    def to_string(self) -> str:
        # TODO: There's a better way to do this 
        c = ", "
        ret = str(self.time_retrieved_utc) + c
        ret += self.type + c + str(self.event_id) + c + self.datetime_utc + c
        ret += str(self.listing_count) + c + str(self.lowest_price_good_deals) + c 
        ret += str(self.lowest_price) + c + str(self.highest_price) + c 
        ret += str(self.visible_listing_count) + c + str(self.median_price) + c 
        ret += self.url + c + str(self.venue_id) + c + str(self.score) + c 
        ret += self.title + c + self.performer0name + c + self.performer1name
        return ret


config = configparser.ConfigParser()
config_filename = "config.cfg"
config.read(config_filename)

CLIENT_ID = config['DEFAULT']['CLIENT_ID']
SECRET = config['DEFAULT']['SECRET']
DATA_FILENAME = config['DEFAULT']['DATA_FILENAME']

if CLIENT_ID == "YOUR_CLIENT_ID_HERE":
    sys.exit("ERROR: Please set CLIENT_ID in config.cfg")


query = 'https://api.seatgeek.com/2/events?performers.slug=colorado-avalanche' + '&client_id=' + CLIENT_ID + '&client_secret=' + SECRET

print(query)

# Getting data
# TODO: Get this data every 15 mins
time_retrieved_utc: datetime.datetime = datetime.datetime.utcnow()
# TODO: Check if this simpler way works
# r = requests.get(query)
# json_data = r.json()

# Additional way to get data
req = urllib.request.Request(query, headers = {'User-Agent':'Mozilla/5.0'})
json_data = json.load(urllib.request.urlopen(req))


# Dump our request to a file for full analysis if necessary
with open('request.txt', 'a') as f:
    f.write(f"{str(time_retrieved_utc)} ;;;; \n {json.dumps(json_data, indent=4)} \n")


for e in json_data['events']:
    es = EventSlice(e, time_retrieved_utc)
    with open(DATA_FILENAME, 'a') as f:
        # TODO: If the file doesn't exist, write a header with the first line
        f.write(es.to_string() + '\n')



    # TODO: let people request via
    # 'https://api.seatgeek.com/2/events?q=boston+celtics'

    # TODO: Ask for only events I'm interested in:
    # 'https://api.seatgeek.com/2/events?id=760304,771261,785673'

    # TODO: Start polling Red Rocks, Coors Field, Fillmore, etc. 

    # TODO: Start to make a visualizer






