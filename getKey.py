#!/usr/bin/env python
# Generates trakt api_key for authorising with trakt
import json 
import trakt
from trakt import init
response = raw_input('Please type in your trakt username here: ')
api_key = init(response)
data = {'api_key': api_key}
with open('trakt-config.json', 'w') as config_file:
	json.dump(data, config_file)
