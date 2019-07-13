#!/usr/bin/env python3

import os
import sys
import argparse
import traceback
from yaml import load
from pymongo import MongoClient
from pprint import pprint

from service.loader import Loader

TEAMS = [
    'ari',    'atl',    'bal',    'bos',
    'chc',    'chw',    'cin',    'cle',
    'col',    'det',    'hou',    'kc',
    'laa',    'lad',    'mia',    'mil',
    'min',    'nym',    'nyy',    'oak',
    'phi',    'pit',    'sd',    'sea',
    'sf',     'stl',    'tb',    'tex',
    'tor',    'wsh'
]

opts = argparse.ArgumentParser(
    description=""
)

opts.add_argument( '-r','--reload',
    action='store_true',
    help='Update data from source for team.')

opts.add_argument( '-l','--load_all',
    action='store_true',
    help='Update data from source for team.')

opts.add_argument( '-t','--team',
    type=str, default='tex',
    #type=str, nargs='+', default='tex',
    help='Team shortname')

arg = opts.parse_args()

client = MongoClient('localhost', 27017)
db = client['mlb_stats_dev']
loader = Loader( db )

if arg.reload:
    loader.load( arg.team )
elif arg.load_all:
    for team in TEAMS:
        loader.load( team )
else:
    loader.get( arg.team )

