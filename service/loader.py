
from lxml import html
import requests
import json
import re
import pytz
from datetime import datetime, timedelta, timezone
from pprint import pprint
from tzlocal import get_localzone
from bson.codec_options import CodecOptions

API_HOST = 'https://site.web.api.espn.com'
SCHED_URI_FMT = """/apis/site/v2/sports/baseball/mlb/teams/{TEAM}/schedule?region=us&lang=en&seasontype={SEASON}"""
LOADER_TS_NAME = 'stats_loader_timestamp'

class Loader:
    def __init__( self, mdbh ):
       self.session = requests.Session()
       self.db = mdbh
       self.tz = get_localzone()
       self.schedule = {}

    def reload_schedule(self, team_sn):
        page = self.session.get( API_HOST +
            SCHED_URI_FMT.format_map({
                'TEAM':   team_sn,
                'SEASON': 2
            }), allow_redirects=True )

        data = json.loads( page.content )

        team_schedule = self.db[team_sn]

        data[LOADER_TS_NAME]    = datetime.utcnow()
        data['stats_loader_sn'] = team_sn

        if data['status'] == 'success':
            del data['status']
            load_id = team_schedule.insert_one( data ).inserted_id
            print( load_id )
            print( self.db.list_collection_names() )
        else:
            raise Exception("Data load failed!");

    def scheduleData(self):
        return self.schedule

    def dump(self):
        for key in self.schedule.keys():
            print( "# " + key )

            if key == 'team':
                pprint( self.schedule[key] )
                next
            elif key == LOADER_TS_NAME:
                print( "Local: %s"%( str( self.schedule[key] ) ))
                utc_time = self.schedule[key].astimezone(pytz.utc)
                print( "UTC:   %s"%( str( utc_time   ) ))
                next
            elif key == 'events':
                for event in self.schedule[key]:
                    #pprint( event )
                    print( '{} {}'.format( event['shortName'], event['date'] ) )
                    for eventKey in event.keys():
                        #if eventKey in  ['','date','shortName']:
                        #    print( '{{{}: {}}}'.format( eventKey, event[eventKey]) )
                        #else:
                        #    print( eventKey )
                        #    pass
                        pass
            elif isinstance( self.schedule[key], dict):
                for key in self.schedule[key].keys():
                    print(" |- " + key )

    def get_schedule( self, team_sn ):
        team_schedule  = self.db[team_sn].with_options(
            codec_options=CodecOptions(
                tz_aware=True,
                tzinfo=self.tz
            )
        )
        oldestData = (datetime.today()-timedelta(hours=2)).astimezone()

        self.schedule = team_schedule.find_one({
                LOADER_TS_NAME: {"$gt": oldestData }
            }, sort=[(LOADER_TS_NAME, -1)] )

        if self.schedule is None:
            print("Reloading schedule, nothing newer than: %s" % (str(oldestData)) )
            self.reload_schedule(team_sn)
            print( "***Data Refreshed***" )
            self.get_schedule(team_sn)
            return
        else:
            print("Data is new than: %s" % (str(oldestData)) )
            pass

