#!/usr/bin/env python3

import os
import sys
import argparse
import traceback
import time
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

opts.add_argument( '-r','--reload_all',
    action='store_true',
    help='Force mongo sync for ALL teams.')

opts.add_argument( '-f','--fresh',
    action='store_true',
    help='Force fresh data for specified team.')

opts.add_argument( '-t','--team',
    type=str, default='tex',
    #type=str, nargs='+', default='tex',
    help='Team shortname (lowercase)')

arg = opts.parse_args()

client = MongoClient('localhost', 27017)
db = client['mlb_stats_dev']
loader = Loader( db )

if arg.reload_all:
    for team in TEAMS:
        loader.reload_schedule( team )
        time.sleep(5)
elif arg.fresh:
    loader.reload_schedule( arg.team )

loader.get_schedule( arg.team )
loader.dump()

