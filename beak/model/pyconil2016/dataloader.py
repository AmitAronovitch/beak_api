import json
import logging
import os.path as op

from dateutil.parser import parse

API_TABLES = [
    ('getLevels', 'levels'),
    ('getLocations', 'locations'),
    ('getSpeakers', 'speakers'),
    ('getTypes', 'types'),
    ('getTracks', 'tracks'),
]


def load():
    thisdir = op.abspath(op.split(__file__)[0])
    jsondir = op.abspath(op.join(thisdir, '..', '..', 'data', 'pyconil2016'))
    logging.debug('checking for data directory at ' + jsondir)
    if not op.isdir(jsondir):
        return

    logging.debug('loading data from json files')
    data = {}
    for cmd, key in API_TABLES:
        jdata = json.load(open(op.join(jsondir, cmd + '.json')))
        table = key[:-1].capitalize()
        data[table] = jdata[key]

    days = json.load(open(op.join(jsondir, 'getSessions.json')))['days']
    events = sum([day['events'] for day in days], [])
    for e in events:
        e["from_"] = parse(e.pop("from"))
        e["to"] = parse(e["to"])
    data['Event'] = events
    return data
