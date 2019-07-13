
from lxml import html
import requests
import json
import re
from datetime import datetime, timedelta, timezone
from pprint import pprint

API_HOST = 'https://site.web.api.espn.com'
SCHED_URI_FMT = """/apis/site/v2/sports/baseball/mlb/teams/{TEAM}/schedule?region=us&lang=en&seasontype={SEASON}"""

class Loader:
    def __init__( self, mdbh ):
       self.session = requests.Session()
       self.db = mdbh

    def load(self, team_sn):
        page = self.session.get( API_HOST +
            SCHED_URI_FMT.format_map({
                'TEAM':   team_sn,
                'SEASON': 2
            }), allow_redirects=True )

        data = json.loads( page.content )

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

        teamstats = self.db[team_sn]

        data['stats_loader_timestamp'] = datetime.utcnow()
        data['stats_loader_sn'] = team_sn

        load_id = teamstats.insert_one( data ).inserted_id

        print( load_id )
        print( self.db.list_collection_names() )

    def get( self, team_sn ):
        teamstats = self.db[team_sn]
        ts_name = 'stats_loader_timestamp'


          #ts_name: {"$gt", (datetime.utcnow()-timedelta(days=1)) }
        oldestData = datetime.today()-timedelta(days=1)
        print( datetime.utcnow() )
        print( oldestData )
        stats = teamstats.find({
            ts_name: {"$gt": oldestData }
          }).sort(ts_name)[0]

        if stats is None:
            self.load(team_sn)
            self.get(team_sn)
            return

        for key in stats.keys():
            print( "# " + key );

            if key == 'team':
                pprint( stats[key] );

            if isinstance( stats[key], dict):
                for key in stats[key].keys():
                    print(" |- " + key )



