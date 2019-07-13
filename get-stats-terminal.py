#!/usr/bin/env python3

import os
import sys
import argparse
import traceback

from yaml import load

from lxml import html
import requests
import json
import re

from pprint import pprint

api_host = 'https://site.web.api.espn.com'
api_uri_fmt = """/apis/site/v2/sports/baseball/mlb/teams/{TEAM}/schedule?region=us&lang=en&seasontype={SEASON}"""

opts = argparse.ArgumentParser(
    description=""
)
opts.add_argument( '-t','--team',
    type=str, default='tex',
    #type=str, nargs='+', default='tex',
    help='Team shortname')

arg = opts.parse_args()

with requests.Session() as session:

    page = session.get( api_host +
        api_uri_fmt.format_map({
            'TEAM':   arg.team,
            'SEASON': 2
        }), allow_redirects=True )

    data = json.loads( page.content )
    #pprint( data );
    print( "\nTop Level Keys:\n" );
    for key in data.keys():
        if isinstance(data[key], dict):
            print( key )
            for layer2 in data[key].keys():
                print( "  " + layer2 )

        if isinstance(data[key], list):
            print( key + " is a list!")
        else:
            print( "{}: {}".format( key, data[key]  ) )

    print( '\nURL: ' + page.url )

