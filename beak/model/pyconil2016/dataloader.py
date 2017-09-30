import os.path as op
import logging, json
from dateutil.parser import parse


def load():
    thisdir = op.abspath(op.split(__file__)[0])
    jsondir = op.abspath(op.join(thisdir,'..','..','data','pyconil2016'))
    logging.debug('checking for data directory at ' + jsondir)
    if not op.isdir(jsondir):
        return
    
    logging.debug('loading data from json files')
    data = {}
    for cmd, key in API_TABLES:
        jdata = json.load(open(op.join(jsondir, cmd+'.json')))
        table = key[:-1].capitalize()
        data[table] = jdata[key]
    
    days = json.load(open(op.join(jsondir, 'getSessions.json')))['days']
    events =  sum([day['events'] for day in days], [])
    for e in events:
        e["from_"] = parse(e.pop("from"))
        e["to"] = parse(e["to"])
    data['Event'] = events
    return data
