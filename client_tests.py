import os
from pprint import pprint

import requests
import pandas as pd
import csv

BASE = 'http://127.0.0.1:5000/api/user_hotspots_stat/{stat}/user/{user_id}'

stats = ['hotspots_quantity',
         'hotspots_with_places_quantity',
         'hotspots_dates',
         'hotspots_scored',
         'hotspots_conns']

users_ids = pd.read_csv(os.path.join('data/users_test.csv'))['id']

for stat in stats:
    for user_id in users_ids.sample(2):
        res = requests.get(BASE.format(stat=stat, user_id=user_id))
        print(res.url)
        pprint(res.json())


res = requests.get(BASE.format(stat='sdfsd', user_id=1))
print(res.url)
pprint(res.json())

res = requests.get(BASE.format(stat='hotspots_quantity', user_id=1))
print(res.url)
pprint(res.json())
