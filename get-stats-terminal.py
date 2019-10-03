#!/usr/bin/env python3

import os
import sys
import argparse
import traceback
import time
import yaml
from pymongo import MongoClient
from pprint import pprint

from mlbstats.service.loader import Loader

DEFAULT_MONGO_HOST = 'localhost'
DEFAULT_MONGO_DB = 'mlb_stats_dev'
DEFAULT_MONGO_PORT = 27017

yourcwd = os.path.realpath('.')
myself  = os.path.basename(__file__)
mydir   = os.path.dirname( __file__)

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

opts.add_argument('-c', '--config', type=str, metavar=f"~/etc/{myself}.yaml", help='Use config file <CONFIG>')

opts.add_argument( '-r','--reload_all',
    action='store_true',
    help='Force mongo sync for ALL teams')

opts.add_argument( '-f','--fresh',
    action='store_true',
    help='Force fresh data for specified team')

opts.add_argument( '-l','--list',
    action='store_true',
    help='List teams')

opts.add_argument( '-t','--teams','--team',
    type=str, nargs='+', metavar=['tex','hou'], default=[],
    help='Team shortname (lowercase)')

opts.add_argument( '--mongoDatabase',
    type=str, metavar=DEFAULT_MONGO_DB, default='',
    help='Use mongo database name')
opts.add_argument( '--mongoHost',
    type=str, metavar=DEFAULT_MONGO_HOST, default='',
    help='Specify mongo host')
opts.add_argument( '--mongoPort',
    type=int, metavar=DEFAULT_MONGO_PORT, default=0,
    help='Specify mongo port')

arg = opts.parse_args()

def cLoader( confFile ):
    try:
        with open( confFile,'r') as stream:
            return yaml.load(stream, Loader=yaml.SafeLoader);
    except Exception as e:
        #print("I require a config file right now...\nFIXME: with reasonable defaults");
        #sys.exit(1)
        return None

conf = {}
if arg.config:
    conf = cLoader( arg.config )
else:
    conf = cLoader( '{}/etc/{}.yaml'.format(mydir, myself) )

if arg.list:
    for team in TEAMS:
        print(f"{team}")
    sys.exit(0)

if not arg.teams and not arg.reload_all:
    opts.print_help()
    sys.exit(1)

if not arg.mongoHost        and (conf is None or 'host'     not in conf['mongo'].keys()):
    arg.mongoHost = DEFAULT_MONGO_HOST
if not arg.mongoPort        and (conf is None or 'port'     not in conf['mongo'].keys()):
    arg.mongoPort = DEFAULT_MONGO_PORT
if not arg.mongoDatabase    and (conf is None or 'database' not in conf['mongo'].keys()):
    arg.mongoDatabase = DEFAULT_MONGO_DB

if not arg.mongoHost: arg.mongoHost = conf['mongo']['host']
if not arg.mongoPort: arg.mongoPort = conf['mongo']['port']
if not arg.mongoDatabase: arg.mongoDatabase = conf['mongo']['database']

client = MongoClient(arg.mongoHost, arg.mongoPort)
db = client[ arg.mongoDatabase ]
loader = Loader( db )

if arg.reload_all:
    for team in TEAMS:
        loader.reload_schedule( team )
        time.sleep(2)
elif arg.fresh:
    for team in arg.teams:
        loader.reload_schedule( team )
        time.sleep(2)

for team in arg.teams:
    loader.get_schedule( team )
    loader.dump()

sys.exit(0)

