#!/usr/bin/env python3

import os
import sys
import argparse
import traceback
import time
import yaml
from pymongo import MongoClient
from pprint import pprint

from service.loader import Loader

yourCwd = os.path.realpath('.')
mySelf  = os.path.basename(__file__)
myDir   = os.path.dirname( __file__)

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

opts.add_argument( '-l','--list',
    action='store_true',
    help='List teams')

opts.add_argument( '-t','--team',
    type=str,
    #type=str, default='tex',
    #type=str, nargs='+', default='tex',
    help='Team shortname (lowercase)')

arg = opts.parse_args()

if arg.list:
    for team in TEAMS:
        print(f"{team}")
    sys.exit(0)

if arg.team is None and not arg.reload_all:
    opts.print_help()
    sys.exit(1)

conf = {}
try:
    with open( '{}/etc/{}.yaml'.format(myDir, mySelf),'r') as stream:
        conf = yaml.load(stream, Loader=yaml.SafeLoader);
except Exception as e:
    print("I require a config file right now...\nFIXME: with reasonable defaults");
    sys.exit(1)
    #pass

print("conf.mongo.host is: %s" % conf['mongo']['host'] );

client = MongoClient(conf['mongo']['host'] or 'localhost', conf['mongo']['port'] or 27017)
db = client[conf['mongo']['database'] or 'mlb_stats_dev']
loader = Loader( db )

if arg.reload_all:
    for team in TEAMS:
        loader.reload_schedule( team )
        time.sleep(5)
elif arg.fresh:
    loader.reload_schedule( arg.team )

loader.get_schedule( arg.team )
loader.dump()

sys.exit(0)
